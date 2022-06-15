import logging

from ScEpTIC import tools
from ScEpTIC.exceptions import ParsingException
from ScEpTIC.AST.elements.instructions.conversion import ConversionOperation
from ScEpTIC.llvmir_parser.sections_parser import global_vars

from . import binary_operations


conversion_operations = [
    'trunc',
    'zext',
    'sext',
    'fptrunc',
    'fpext',
    'fptoui',
    'fptosi',
    'uitofp',
    'sitofp',
    'ptrtoint',
    'inttoptr',
    'bitcast',
    'addrspacecast'
]

def parse_conversion_operation(text, has_target = True):
    """
    Parses and returns a conversion operation.
    %target = op_code <type> <value> to <type>
    """

    logging.debug('Calling parse_conversion_operation({}, {})'.format(text, has_target))

    if not is_conversion_operation(text, has_target):
        raise ParsingException('Conversion operation (trunc,zext,sext,fptrunc,fpext,fptoui,fptosi,uitofp,sitofp,ptrtoint,inttoptr,bitcast,addrspacecas) expected.\n{} given.'.format(text))
    
    target = None
    offset = 0

    # retrieve where the result must be stored
    if has_target:
        target, offset = binary_operations.parse_result_target(text)
    
    operation_code = text[offset]

    if not has_target and text[1] == '(' and text[-1] == ')':
        text = text[1:-1]

    # split source and target
    separating_token = 'to'
    text = tools.split_into_sublist(text[offset+1:], separating_token)

    source_grp = text[0]
    target_grp = text[1]
    
    source_value = binary_operations.parse_operand(source_grp, True)

    target_type = global_vars.parse_type(target_grp)

    return ConversionOperation(operation_code, source_value, target_type, target)


def is_conversion_operation(text, has_target = True):
    """
    Return if an instruction is a conversion operation.
    """

    logging.debug('Calling is_conversion_operation({}, {})'.format(text, has_target))

    if len(text) < 4:
        return False

    if not has_target:
        return text[0] in conversion_operations

    return text[0] == '%' and text[2] == '=' and text[3] in conversion_operations
