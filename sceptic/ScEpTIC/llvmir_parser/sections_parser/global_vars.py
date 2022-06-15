import logging

from ScEpTIC import tools
from ScEpTIC.AST.elements.global_var import GlobalVar
from ScEpTIC.AST.elements.types import Type, BaseType
from ScEpTIC.AST.elements.value import Value
from ScEpTIC.exceptions import ParsingException, LLVMSyntaxErrorException, NotImplementedException
from ScEpTIC.llvmir_parser.token_generator import TOKEN_SPACE

from ScEpTIC.llvmir_parser.instructions_parser import binary_operations
from ScEpTIC.llvmir_parser.instructions_parser import memory_operations

from . import custom_types
from . import metadata


def parse_global_vars_section(text, log_section_content = False):
    """
    Parses and returns the global variables section, using parse_global_var.
    @<GlobalVarName> = [Linkage] [PreemptionSpecifier] [Visibility]
                       [DLLStorageClass] [ThreadLocal]
                       [(unnamed_addr|local_unnamed_addr)] [AddrSpace]
                       [ExternallyInitialized]
                       <global | constant> <Type> [<initial_valConstant>]
                       [, section "name"] [, comdat [($name)]]
                       [, align <Alignment>] (, !name !N)*
    """

    logging.debug('Calling parse_global_var_section({}, {})'.format(text, log_section_content))

    for line in text:
        parse_global_var(line)
    
    global_vars = GlobalVar.elements

    if logging.getLogger().isEnabledFor(logging.INFO):
        log_str = 'Parsed global variables section. {} global variables found'.format(len(global_vars))

        if log_section_content:
            log_str += ':\n{}'.format(tools.fancy_dict_to_str(global_vars))
        else:
            log_str += '.\n{}'.format(tools.fancy_dict_keys_to_str(global_vars))

        logging.info(log_str)
    
    return global_vars


def parse_global_var(text):
    """
    Parses a line containing the definition of a global variable and returns it.
    """

    logging.debug('Calling parse_global_var({})'.format(text))

    if not is_global_var_def(text):
        raise ParsingException('Invalid global variable definition! Global variables must start with @')
    
    name = "@"+text[1]

    # attributes are separated by comma
    # text[3:] removes ['@', 'name', '=']
    # if an array is initialized, it will be like [i32 val, i32 val2, ...]
    # so elements inside [...] must not be splitted using commas.
    # use [] and () due to getelementptr
    elements = text[3:]
    str_def = tools.get_indexes_of_matching_tokens(elements, 'c"', '"')

    # fix for string initialization
    if str_def is not None:
        elements = elements[0:str_def[0]] + [elements[str_def[0]:str_def[1]]] + elements[str_def[1]:]

    attributes = tools.split_context_into_sublist(elements, ",")

    # parse main attributes part
    retval = parse_main_attributes(attributes[0])
    retval['name'] = name
    attributes = attributes[1:]

    # parse section part
    section = parse_section_attribute(attributes[0])
    if section is not None:
        attributes = attributes[1:]
    retval['section'] = section

    # parse comdat part
    comdat = parse_comdat_attribute(attributes[0])
    if comdat is not None:
        attributes = attributes[1:]
    retval['comdat'] = comdat
        
    # parse align part
    align = parse_align_attribute(attributes[0])
    if align is not None:
        attributes = attributes[1:]
    retval['align'] = align

    # parse all metadatas
    retval['metadata'] = metadata.get_element_metadata(tools.flat_list(attributes), 'global variable {}'.format(retval['name']))

    if logging.getLogger().isEnabledFor(logging.DEBUG):
        log_vals = " {}".format(retval)
        logging.debug('Parsed global variable {}:\n{}'.format(name, tools.instert_new_line_every(log_vals, new_line_padding = ' ')))
    
    retval = GlobalVar(retval['name'], retval['type'], retval['initial_val'], retval['is_constant'], retval['align'], retval['section'], retval['comdat'], retval['metadata'])

    return retval
    

def parse_main_attributes(text):
    """
    Parses the main and mandatory attributes of the variable (type, initial value).
    Returns a dictionary containing the relevant information of the variable.
    """

    logging.debug('Calling parse_main_attributes({})'.format(text))

    if 'global' in text:
        start = text.index('global')

    elif 'constant' in text:
        start = text.index('constant')

    else:
        raise LLVMSyntaxErrorException('Mandatory Global / Constant attribute not found!')

    type_and_init = text[start+1:]
    
    retval = parse_type_and_initial_val(type_and_init)
    retval['is_constant'] = text[start] == 'constant'

    # Those attributes are not important for my simulation
    # [Linkage] [PreemptionSpecifier] [Visibility] [DLLStorageClass] [ThreadLocal]
    # [(unnamed_addr|local_unnamed_addr)] [AddrSpace] [ExternallyInitialized]
    optional_attributes = text[:start]
    retval['optional_attributes'] = optional_attributes

    return retval


def parse_type_and_initial_val(text):
    """
    Returns the type and the initial_val (if any) of the variable
    """

    logging.debug('Calling parse_type_and_initial_val({})'.format(text))
    
    parentheses_groups = tools.split_parantheses_groups_with_context(text)
    must_be_array = False
    
    # is an array, for shure.
    if len(parentheses_groups) > 1:
        text = parentheses_groups[0]
        initial_val = parse_array_initial_val(parentheses_groups[1])
        
        if initial_val == 'zeroinitializer':
            initial_val = Value('immediate', initial_val, None)

        else:
            initial_val = Value('array_val', initial_val, None)

        must_be_array = True

    elif 'getelementptr' in text:
        index = text.index('getelementptr')
        pointer_val = memory_operations.parse_getelementptr_operation(text[index:], False)
        initial_val = Value('address', pointer_val, None)
        text = text[:index]

    else:
        # not an array, or array not initialized
        value = text[-1]
        if is_valid_initial_val(value):
            text = text[:-1]
        else:
            value = None

        initial_val = Value('immediate', value, None)

    retval = {'type': parse_type(text), 'initial_val': initial_val}

    initial_val.type = retval['type']

    if must_be_array and not retval['type'].is_array:
        raise ParsingException('Array initialization vector given. Type must be an array. {} given'.format(text))

    return retval


def is_valid_initial_val(text):
    """
    Verify if text is a valid initial_val.
    Admitted initial_vals:
        - 0.00e+000
        - 0.0
        - null
        - zeroinitial_val
    """

    logging.debug('Calling is_valid_initial_val({})'.format(text))

    if 'e+' in text:
        return True

    if '0x' in text:
        return True

    if 'zeroinitializer' == text:
        return True

    if 'null' == text:
        return True

    try:
        float(text)
        return True

    except ValueError:
        pass

    return False


def parse_array_initial_val(text):
    """
    Parses the array initial value and returns it. It also works for vectors.
    It can be a list of values or a list of sub-lists.
    It is a list (n-dimension, as the array initialization vector).
    """

    logging.debug('Calling parse_array_initial_val({})'.format(text))
    initial_vals = []
    force_zero_par = False

    if text.count('[') != text.count(']'):
        raise LLVMSyntaxErrorException('Unbalanced number of [] parentheses for initial value of array: {}'.format(text))

    if isinstance(text, list) and len(text) == 1 and isinstance(text[0], list):
        text = tools.list_replace_element(text[0], TOKEN_SPACE, ' ')
        force_zero_par = True

    if text.count('[') == 0 or force_zero_par:
        if text[0] == 'zeroinitializer' or (text[0] == '*' and text[1] == 'null'):
            initial_vals = 'zeroinitializer'

        elif text[0] == 'c' and text[1] == '"' and text[-1] == '"':
            # get initialization string content
            text = tools.list_to_string(text[2:-1])

            i = 0

            while i < len(text):
                element = text[i]
                
                if element == '\\':
                    element = tools.list_to_string(text[i+1:i+3])
                    element = int(element, 16)

                    i += 2

                else:
                    element = ord(element)
                    
                element = Value('immediate', element, 'char')
                initial_vals.append(element)

                i += 1

        else:
            raise ParsingException('Array initialization string c"string_value" or zeroinitializer expected. {} given'.format(text))

    elif text.count('[') == 1:
        # just a list of values. Get the elements and parse them
        # e.g [i32 0, i32 1, ...]
        start, end = tools.get_list_boundaries(text, '[', ']')
        text = tools.split_context_into_sublist(text[start:end], ',', ['{'], ['}'])

        for initial_val in text:
            if '{' in initial_val and '}' in initial_val and ',' in initial_val:
                start, end = tools.get_list_boundaries(initial_val, '{', '}')
                sub_text = tools.split_into_sublist(initial_val[start:end], ',')

                for initial_val in sub_text:
                    initial_val = binary_operations.parse_operand(initial_val, True)
                    initial_vals.append(initial_val)

            else:
                initial_val = binary_operations.parse_operand(initial_val, True)
                initial_vals.append(initial_val)

    else:
        # array 2+ dimensional.
        # is a list of list (of list)*
        
        # remove the external [] and divide into sublists
        start, end = tools.get_list_boundaries(text, '[', ']', True)
        text = tools.split_context_into_sublist(text[start:end], ',')
        
        for val_grp in text:
            # for each sublist we have [n x type] [ list of type-value ]
            # those lines get the list of type-value and parse it.
            val_grp = tools.split_parantheses_groups(val_grp)
            initial_val = parse_array_initial_val(val_grp[1])
            initial_vals.append(initial_val)

    return initial_vals


def parse_type(text, is_function_return_type = False, is_function_attr = False):
    """
    Parses and returns the type of a given operand/variable.
    """

    logging.debug('Calling parse_type({}, {}, {})'.format(text, is_function_return_type, is_function_attr))
    
    parsed_type = Type.empty()

    # bitcast or other conversion to point to a defined data structure
    # the data structure can be ignored, since is specified in other places
    if (text[0] == '{' or text[0] == '[' or text[0] == '<') and text[-1] == '*':
        parsed_type.is_pointer = True
        parsed_type.pointer_level = text.count('*')

        # dummy value. It will be correctly replaced by the AST with the dimension of the address
        # NB: pointer's dimension to a 32bit integer is the same of the dimension of a pointer to a 64bit double
        # since they contains not the data, but an address to where data is placed.
        text = ['i32']

    # Struct / Union explicit definition
    elif text[0] == '{':
        parsed_type.is_base_type = False
        parsed_type.is_ct_defined = True
        parsed_type.custom_type_def = custom_types.parse_type_composition(['type'] + text)

    # n-dimensional Array
    elif text[0] == '[':
        array_elements, parsed_type = parse_array_def(text)
        parsed_type.is_array = True
        parsed_type._set_array_composition(array_elements)

    # vector type
    elif text[0] == '<':
        # < 2 x i32 >
        parsed_type.is_vector = True
        parsed_type.vector_dimension = int(text[1])
        # actual type is on position 3 (4th token)
        text = text[3]

    else:
        # If pointer, count the level
        if '*' in text:
            parsed_type.is_pointer = True
            parsed_type.pointer_level = text.count('*')
            text = tools.list_sanitize(text, '*')
        
        # Struct / Union
        if text[0] == '%':
            parsed_type.is_base_type = False
            parsed_type.custom_type_name = text[0]+text[1]

    # if it is neither an array, nor a struct/union, it is a base type
    if not parsed_type.is_array and parsed_type.is_base_type:
        if isinstance(text, list):
            text = text[0]
        
        parsed_type.base_type = parse_base_type(text, is_function_return_type, is_function_attr)

    return parsed_type


def parse_base_type(text, is_function_return_type = False, is_function_attr = False):
    """
    Returns the base type of a variable (type and bits)
    """

    logging.debug('Calling parse_base_type({}, {}, {})'.format(text, is_function_return_type, is_function_attr))

    fp_bits = {'half': 16, 'float': 32, 'double': 64, 'fp128': 128, 'x86_fp80': 80, 'ppc_fp128': 128}

    # float and derivates
    if text in fp_bits:
        return BaseType('float', fp_bits[text])

    # integer / bits derivates
    if text[0] == 'i':
        return BaseType('int', text[1:])

    if is_function_return_type and text == 'void':
        return BaseType('void', '0')

    if is_function_attr:
        if text == 'metadata':
            return BaseType('metadata', '0')

        elif text == '...':
            return BaseType('var_args', '8')

    raise NotImplementedException('Numeric type {} not implemented!'.format(text))


def parse_array_def(text):
    """
    Returns the type of the array and its dimensionality
    """

    logging.debug('Calling parse_array_def({})'.format(text))

    # an array definition must start with [ and end with ]
    # if is a string will be [...] c"..."
    if text[0] != '[' or text[-1] != ']':
        raise LLVMSyntaxErrorException('Array expected! {} given'.format(text))
    
    # remove [ and ]
    text = text[1:-1]

    # ['number', 'x', 'type']
    elements_number = [text[0]]
    elements_type = text[2:]

    # if the array is n+1 dimensions, parse it.
    if elements_type[0] == '[':
        subvec_elements_number, subvec_elements_type = parse_array_def(elements_type)
        # concatenate two lists, to have a flat one
        elements_number = elements_number + subvec_elements_number
        # overwrite the array type with the one found recursively
        elements_type = subvec_elements_type

    else:
        # the array dimensionality has been processed. Now get the actual type
        elements_type = parse_type(elements_type)

    return elements_number, elements_type


def parse_section_attribute(text):
    """
    Check and returns the value of the section attribute.
    If not present, returns false
    """

    logging.debug('Calling parse_section_attribute({})'.format(text))

    if 'section' not in text:
        logging.debug('Section attribute not present.')
        return None

    # ['section', '"', 'section_name', '"']
    # get only section_name
    start, end = tools.get_list_apex_boundaries(text)
    
    # convert to string
    section = tools.list_to_string(text[start:end], {TOKEN_SPACE: ' '})
    
    return section


def parse_comdat_attribute(text):
    """
    Check and returns the value of the comdat attribute.
    If not present, returns false
    """

    logging.debug('Calling parse_comdat_attribute({})'.format(text))

    if 'comdat' not in text:
        logging.debug('Comdat attribute not present.')
        return None

    index = text.index('comdat')
    comdat = text[index+1:]
    
    # if is comdat(...) get the part inside ()
    if(comdat[0] == '('):
        comdat = comdat[1:-1]

    comdat = tools.list_to_string(comdat, {TOKEN_SPACE: ' '})

    return comdat


def parse_align_attribute(text):
    """
    Check and returns the value of the align attribute.
    If not present, returns false
    """

    logging.debug('Calling parse_align_attribute({})'.format(text))

    if 'align' not in text:
        logging.debug('Align attribute not present.')
        return None

    index = text.index('align')
    align = text[index+1]

    return align


def is_global_var_def(text):
    """
    Returns if the current line is a global variable definition.
    """

    logging.debug('Calling is_global_var_def({})'.format(text))

    return isinstance(text, list) and len(text) > 3 and text[0] == '@' and text[2] == '='
