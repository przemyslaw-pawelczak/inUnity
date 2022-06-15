import logging

from ScEpTIC import tools
from ScEpTIC.AST.elements.types import CustomType
from ScEpTIC.exceptions import ParsingException, LLVMSyntaxErrorException, NotImplementedException

from . import global_vars

# Token used to separate type and name
# e.g. stuct.mystructname / union.myunionname
TYPE_NAME_SEPARATOR_TOKEN = '.'

def parse_custom_types_section(text, log_section_content = False):
    """
    Parses and returns the custom types section, using parse_custom_type_definition.
    %type_type.type_name = type { type_name (, type_name)* }
    """

    logging.debug('Calling parse_custom_types_section({}, {})'.format(text, log_section_content))

    for line in text:
        # automatically appended, so no need to save value
        parse_custom_type_definition(line)

    custom_types = CustomType.elements
    
    if logging.getLogger().isEnabledFor(logging.INFO):
        log_str = 'Parsed custom types section. {} custom types found'.format(len(custom_types))

        if log_section_content:
            log_str += ':\n{}'.format(tools.fancy_dict_to_str(custom_types))
        else:
            log_str += '.\n{}'.format(tools.fancy_dict_keys_to_str(custom_types))

        logging.info(log_str)

    return custom_types


def parse_custom_type_definition(text):
    """
    Parses and returns a type declaration.
    """

    logging.debug('Calling parse_custom_type_definition({})'.format(text))
        
    if not is_custom_type(text):
        raise ParsingException('Custom type definition expected. {} given.'.format(text))

    retval = parse_name_and_type(text[1])

    # get the body of the declaration and parse it
    type_declaration = text.index('type')
    retval['composition'] = parse_type_composition(text[type_declaration:])

    if logging.getLogger().isEnabledFor(logging.DEBUG):
        log_vals = " {}".format(retval)
        logging.debug('Parsed type definition {}:\n{}'.format(retval['text'], tools.instert_new_line_every(log_vals, new_line_padding = ' ')))
    
    retval = CustomType(retval['text'], retval['type'], retval['name'], retval['composition'])

    return retval


def parse_name_and_type(text):
    """
    Parses and returns the type (union or struct) and the name of the new declared type.
    """

    logging.debug('Calling parse_name_and_type({})'.format(text))

    # in C only union and struct can be declarated as composed types
    supported_types = ['union', 'struct']

    # if no separator -> the type declaration is not correct
    if TYPE_NAME_SEPARATOR_TOKEN not in text:
        raise ParsingException('Type declaration "{}" is not supported!'.format(text))

    # split to get the type and the name
    tmp = text.split('.')

    retval = {'type': tmp[0], 'name': tmp[1], 'text': '%'+text}

    # only supported types
    if retval['type'] not in supported_types:
        raise NotImplementedException('Type "{}" is not supported!'.format(retval['type']))

    return retval


def parse_type_composition(text, is_from_function = False):
    """
    Parses and return the type composition of the type declaration.
    Elements are parsed using the global_var "parse_type" implementation.
    """

    logging.debug('Calling parse_type_composition({}, {})'.format(text, is_from_function))

    # type declaration must be type { ... }
    if text[0] != 'type' or text[1] != '{' or text[-1] != '}':
        raise LLVMSyntaxErrorException('Type composition expected. {} given.'.format(text))

    # split the list using comma, that is the separator between subsequents types
    text = tools.split_into_sublist(text[2:-1], ",")
    retval = []

    for sub_type in text:
        retval.append(global_vars.parse_type(sub_type, is_from_function))

    return retval


def is_custom_type(text):
    """
    Returns if the current line is a type definition.
    """

    logging.debug('Calling is_custom_type({})'.format(text))
    
    if isinstance(text, list) and len(text) > 0 and text[0] == '%':
        try:
            text.index('type')
            return True
        except ValueError:
            pass

    return False
