import logging

from ScEpTIC import tools
from ScEpTIC.AST.elements.function import Function
from ScEpTIC.AST.elements.instructions.other_operations import CallOperation
from ScEpTIC.AST.elements.metadata import Metadata
from ScEpTIC.exceptions import ParsingException, LLVMSyntaxErrorException
from ScEpTIC.llvmir_parser import instructions_parser

from . import custom_types
from . import global_vars
from . import metadata


def parse_function_declarations_section(text, log_section_content = False):
    """
    Parses and returns the function declaration section, using parse_function_definition.
    <define|declare> [linkage] [PreemptionSpecifier] [visibility] [DLLStorageClass]
           [cconv] [ret attrs]
           <ResultType> @<FunctionName> ([argument list])
           [(unnamed_addr|local_unnamed_addr)] [fn Attrs] [section "name"]
           [comdat [($name)]] [align N] [gc] [prefix Constant]
           [prologue Constant] [personality Constant] (!name !N)* { ... }
    """

    logging.debug('Calling parse_function_declaration_section({}, {})'.format(text, log_section_content))
    
    function_decls = Function.declarations

    for line in text:
        parse_function_declaration(line)
        
    if logging.getLogger().isEnabledFor(logging.INFO):
        log_str = 'Parsed function declarations section. {} function declarations found'.format(len(function_decls))

        if log_section_content:
            log_str += ':\n{}'.format(tools.fancy_dict_to_str(function_decls))
        else:
            log_str += '.\n{}'.format(tools.fancy_dict_keys_to_str(function_decls))

        logging.info(log_str)

    return function_decls


def parse_function_definition_section(text, log_section_content = False):
    """
    Parses and returns the function definition section, using parse_function_definition and parse_function_body.
    """

    logging.debug('Calling parse_function_definition_section({}, {})'.format(text, log_section_content))
    
    for line in text:
        parse_function_definition(line['def'], line['body'])

    function_defs = Function.elements

    if logging.getLogger().isEnabledFor(logging.INFO):
        log_str = 'Parsed function definition section. {} function definition found'.format(len(function_defs))
        
        if log_section_content:
            log_str += ':\n'
            
            for f_def in function_defs.values():
                log_str += '{}\n\n'.format(f_def)

        else:
            log_str += '.\n{}'.format(tools.fancy_dict_keys_to_str(function_defs))

        logging.info(log_str)

    return function_defs


def parse_function_definition(declaration, body):
    """
    Parses and returns a function definition, which consists in the function declaration and the function body.
    """

    logging.debug('Calling parse_function_definition({}, {})'.format(declaration, body))

    declaration = parse_function_declaration(declaration)
    body = parse_function_body(body, declaration)
    
    declaration.attach_body(body)


def parse_function_declaration(text):
    """
    Parses a line containing a function intestation and returns it.
    """

    logging.debug('Calling parse_function_declaration({})'.format(text))

    def_type = text[0]
        
    # define is always the first token
    if def_type not in ['define', 'declare']:
        raise ParsingException('define or declare token expected. {} given'.format(text[0]))

    if def_type == 'define' and text[-1] != '{':
        raise LLVMSyntaxErrorException('Function body not present for function definition!')

    # name always starts with @
    # before @ there is always the return type
    # after @ there is always the name
    try:
        name_identifier_position = text.index('@')
    except ValueError:
        raise ParsingException('Function name delimiter not present')

    name = '@'+text[name_identifier_position+1]

    if is_llvm_dbg(name):
        return None
    
    # parse return type and get delimiter for optional attributes
    return_type, optional_delimiter = parse_return_type(text[:name_identifier_position])
    
    try:
        start = text.index('(')+1
        # due to parameter attributes, () can be inside other ()
        # get the last )
        end = tools.list_rindex(text, ')')

    except ValueError:
        raise ParsingException('Unable to find function argument delimiters!')

    arguments = parse_function_arguments(text[start:end])

    # remove parsed elements
    text = text[end+1:]

    attr_groups = get_function_attributes_group(text)

    f_metadata = metadata.get_element_metadata(text, "declaration of function {}".format(name))

    retval = Function(name, return_type, arguments, attr_groups, f_metadata)
    
    if logging.getLogger().isEnabledFor(logging.DEBUG):
        log_vals = " {}".format(retval)
        logging.debug('Parsed function {} {}:\n{}'.format('definition' if def_type == 'define' else 'declaration', name, tools.instert_new_line_every(log_vals, new_line_padding = ' ')))
    
    return retval


def parse_function_body(text, declaration):
    """
    Parses and returns the function body as a list of instructions.
    """

    function_name = declaration.name
    logging.debug('Calling parse_function_body({}, {})'.format(text, function_name))
    
    body = []
    
    i = 0

    # used for select operation
    basic_block_id = declaration.first_basic_block_id

    label = None
    
    while i < len(text):
        line = text[i]

        # if is label, parse it and update the basic_block_id
        if is_label(line):
            label = parse_label(line)
            basic_block_id = label['label']

            # go to next line to attach the label
            i += 1
            line = text[i]
        
        elif label is None:
            label = {'label': None, 'preds': None}

        instruction = instructions_parser.parse_instruction(line, i, function_name)

        # unreachable instruction returns None
        if instruction is None:
            i += 1
            continue

        instruction.basic_block_id = basic_block_id
        instruction.label = label['label']
        instruction.preds = label['preds']

        # parse special debug functions.
        if is_llvm_dbg(instruction):
            handle_llvm_dbg(instruction, body)

        else:
            body.append(instruction)
            # remove label, otherwise is attached to next element
            label = None

        i += 1

    # set first element label
    body[0].label = declaration.first_basic_block_id

    return body


def parse_return_type(text):
    """
    Parses the return type of the function.
    Returns a list representing the types returned by the function and the
    delimiter of the type definition.
    Uses both custom_types and global_vars parse functions
    """

    logging.debug('Calling parse_return_type({})'.format(text))
    
    last_char = text[-1]

    composition = None
    
    delimiter = len(text)-1

    if last_char == '*':
        # returns a pointer
        return_type = text[-2:]
        delimiter -= 1

    elif last_char == '}':
        # returns a struct
        # find where starting { is. Remove ending { from search
        # note: if a struct is too big, it will be passed as argument instead of return type
        
        index = text.index('{')
        delimiter = index

        return_type = text[index+1:-1]
        
        # format as a struct definition
        return_type = ['type', '{'] + return_type + ['}']

        composition = custom_types.parse_type_composition(return_type, True)

    else:
        return_type = [last_char]

    if composition is None:
        composition = [global_vars.parse_type(return_type, True)]

    return composition, delimiter


def parse_function_arguments(text):
    """
    Returns the list of the arguments of the function.
    """

    logging.debug('Calling parse_function_arguments({})'.format(text))

    # arguments separated by ,
    arguments = tools.split_into_sublist(text, ',')

    ret_args = []
    for arg in arguments:
        type_def, attributes = extract_type_and_attributes(arg)
        
        # parse type as variables
        arg = global_vars.parse_type(type_def, is_function_attr=True)
        arg.attributes = attributes
        
        ret_args.append(arg)

    return ret_args


def extract_type_and_attributes(text):
    """
    This function separates parameter attributes from the parameter type.
    """

    logging.debug('Calling parse_function_arguments({})'.format(text))

    parameter_attributes = ['zeroext', 'signext', 'inreg', 'byval', 'inalloca', 'sret', 'noalias', 'nocapture', 'nest', 'returned', 'nonnull', 'swiftself', 'swifterror']
    
    # align <n>
    # dereferenceable(<n>)
    # dereferenceable_or_null(<n>)
    multi_arg_attributes = ['align', 'dereferenceable', 'dereferenceable_or_null']
    
    type_def = []
    attributes = []

    i = 0
    
    while i < len(text):
        element = text[i]

        if element in parameter_attributes:
            attributes.append(element)
        
        elif element in multi_arg_attributes:
            if element == 'align':
                i += 1
                val = text[i]
            else:
                # skip (
                i += 2
                val = text[i]
                # skip )
                i += 1

            attributes.append({element: val})

        else:
            # not an attribute
            type_def.append(element)

        i += 1

    return type_def, attributes


def get_function_attributes_group(text):
    """
    Returns the list of attributes groups the function has.
    """

    logging.debug('Calling get_function_attributes_group({})'.format(text))

    attr_groups = []

    offset = 0
    
    token = '#'

    while token in text[offset:]:
        # get index of element after #
        index = text.index(token, offset) + 1

        attr_groups.append(text[index])

        offset = index

    return attr_groups


def is_function_definition(text):
    """
    Returns if a given line is a function definition.
    """

    logging.debug('Calling is_function_definition({})'.format(text))

    return isinstance(text, list) and len(text) > 1 and text[0] == 'define' and text[-1] == '{'


def is_function_declaration(text):
    """
    Returns if a given line is a function declaration.
    """

    logging.debug('Calling is_function_declaration({})'.format(text))

    return isinstance(text, list) and len(text) > 1 and text[0] == 'declare'


def is_label(text):
    """
    Returns if a line represents a label.
    [';', '<', 'label', '>', ':', '17', ':', ';', 'preds', '=', '%', '7']
    """

    logging.debug('Calling is_label({})'.format(text))

    if len(text) < 5:
        return False

    return text[0] == ';' and text[1] == '<' and text[2] == 'label' and text[3] == '>' and text[4] == ':'


def parse_label(text):
    """
    Parses a label.
    """

    logging.debug('Calling is_label({})'.format(text))

    if not is_label(text):
        raise ParsingException('Label expected. {} given'.format(text))

    index = text.index(':') + 1
    label_id = '%'+text[index]
    text = text[index+1:]
    
    preds = []
        
    if 'preds' in text:
        index = text.index('=') + 1
        text  = tools.split_into_sublist(text[index:], ',')

        for pred in text:
            if pred[1] != '0':
                preds.append('%'+pred[1])

    return {'label': label_id, 'preds': preds}


def is_llvm_dbg(instruction, check_if_string = True):
    """
    Returns if an instruction is a call to a llvm.dbg function.
    """

    logging.debug('Calling is_llvm_dbg({}, {})'.format(instruction, check_if_string))

    names = ['@llvm.dbg.addr', '@llvm.dbg.declare', '@llvm.dbg.value']

    if check_if_string and isinstance(instruction, str):
        return instruction in names

    return isinstance(instruction, CallOperation) and instruction.name in names


def handle_llvm_dbg(instruction, body):
    """
    Handles the llvm.dbg function.
    It just appends metadata to the designed instruction.
    """

    logging.debug('Calling handle_llvm_dbg_addr({})'.format(instruction))
    
    if not is_llvm_dbg(instruction, False):
        raise ParsingException('@llvm.dbg.addr, @llvm.dbg.declare, @llvm.dbg.value expected, {} given.'.format(instruction))

    # llvm dbg value can be skipped. used only when code is optimized.
    if instruction.name == '@llvm.dbg.value':
        return None

    args = instruction.function_args

    if len(args) != 3:
        raise ParsingException('3 function arguments expected. {} given'.format(len(args)))

    target = args[0].value
    include_metadata = [args[1].value, args[2].value]

    if instruction.metadata is not None:
        include_metadata.extend(instruction.metadata.includes)

    for instr in body:
        if instr.target is not None and instr.target.value == target:

            if instr.metadata is not None:
                instr.metadata.includes.extend(include_metadata)

            else:
                instr.metadata = Metadata(None, 'collection', 'collection', [], include_metadata)

            break
