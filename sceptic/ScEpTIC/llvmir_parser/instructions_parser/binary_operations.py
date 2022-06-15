import logging

from ScEpTIC import tools
from ScEpTIC.AST.elements.instructions.binary_operation import BinaryOperation
from ScEpTIC.AST.elements.value import Value
from ScEpTIC.exceptions import ParsingException
from ScEpTIC.llvmir_parser.sections_parser import global_vars

from . import memory_operations
from . import conversion_operations


def parse_binary_operation(text):
    """
    Parses and returns a binary operation.

    Binary Operations:
        - add
        - fadd
        - sub
        - fsub
        - mul
        - fmul
        - udiv
        - sdiv
        - fdiv
        - urem
        - srem
        - frem

    Bitwise Binary Operations:
        - shl
        - lsrh
        - asrh
        - and
        - or
        - xor

    %target = <opcode> [optional_attributes] <type> <operand_1>, <operand_2>
    """

    logging.debug('Calling parse_binary_operation({})'.format(text))

    if not is_binary_operation(text):
        raise ParsingException('Binary operation (add, fadd, sub, fsub, mul, fmul, udiv, sdiv, fdiv, urem, srem, frem) expected.\n{} given'.format(text))

    # get the target virtual register and the offset from which the actual operation start
    target, offset = parse_result_target(text)
    # get the operation code
    op_code = text[offset]
    # remove parsed stuff
    text = text[offset+1:]

    # parse specific attributes
    specific_attr_parser = get_specific_attr_parser(op_code)
    
    if specific_attr_parser is not None:
        specific_attr, text = specific_attr_parser(text, op_code)

    else:
        specific_attr = []

    operands = parse_type_and_operands(text)
    bitwise = is_bitwise(op_code)

    return BinaryOperation(op_code, operands['op1'], operands['op2'], target, bitwise, specific_attr)


def is_binary_operation(text):
    """
    Returns if a given instruction is a binary operation.
    """

    logging.debug('Calling is_binary_operation({})'.format(text))
    
    if len(text) < 4:
        return False

    supported_bin_ops = [
        'add',
        'fadd',
        'sub',
        'fsub',
        'mul',
        'fmul',
        'udiv',
        'sdiv',
        'fdiv',
        'urem',
        'srem',
        'frem',
        'shl',
        'lshr',
        'ashr',
        'and',
        'or',
        'xor'
    ]

    op_code = text[3]

    correct_op_code = op_code in supported_bin_ops

    return correct_op_code and text[0] == '%' and text[2] == '='


def is_bitwise(operation_code):
    """
    Returns if a given istruction is a bitwise binary operation.
    """

    logging.debug('Calling is_binary_operation({})'.format(operation_code))

    bitwise_codes = ['shl', 'lshr', 'ashr', 'and', 'or', 'xor']

    return operation_code in bitwise_codes


def get_specific_attr_parser(op_code):
    """
    Returns the optional parser for specific attributes.
    """

    logging.debug('Calling get_specific_attr_parser({})'.format(op_code))

    if op_code in ['add', 'sub', 'mul', 'shl']:
        return parse_int_specific_attr

    elif op_code in ['fadd', 'fsub', 'fmul', 'fdiv', 'frem']:
        return parse_fp_specific_attr

    elif op_code in ['udiv', 'sdiv', 'lshr', 'ashr']:
        return parse_int_div_specific_attr


def parse_result_target(text):
    """
    Returns the target virtual register of the result and the offset of the text.
    """

    logging.debug('Calling parse_result_target({})'.format(text))

    if text[0] != '%' or text[2] != '=':
        raise ParsingException('Invalid result target: %virtual_reg = expected. {} given.'.format(text))

    # %vreg = ...
    # 3 to remove % vreg =
    offset = 3
    
    target = parse_operand(text[0:2])
    
    return target, offset


def parse_type_and_operands(text):
    """
    Parses type and operands of a binary operation. It returns a dict with keys {'op1', 'op2'}
    """

    logging.debug('Calling parse_type_and_operands({})'.format(text))

    text = tools.split_context_into_sublist(text, ',')

    if len(text) != 2:
        raise ParsingException('Operands len must be 2! Parsed operands: {}'.format(text))

    op1 = parse_operand(text[0], True)
    op2 = parse_operand(text[1])
    op2.type = op1.type

    return {'op1': op1, 'op2': op2}


def extract_type(text, is_function_return_type = True, is_function_attr = True):
    """
    Returns the type and the offset of the type in a given string.
    """

    logging.debug('Calling extract_type({}, {}, {})'.format(text, is_function_return_type, is_function_attr))
    
    metadata_offset = 0

    # if is metadata, remove keyword only if it does not refer to a metadata element
    if text[0] == 'metadata' and text[1] != '!':
        text = text[1:]
        metadata_offset = 1

    if text[0] == '<':
        # is vector
        end = text.index('>')
        element_type = text[:end+1]
        offset = end + 1

    elif text[0] == '%':
        # is struct / union
        element_type = text[:2]
        offset = 2

    elif text[0] == '[':
        # is an array
        end = tools.get_index_of_closed_par(text, '[', ']')
        element_type = text[:end+1]
        offset = end + 1
        
    elif text[0] == '{':
        # is a type composition
        end = tools.get_index_in_context(text, '}')
        element_type = text[:end+1]
        offset = end + 1

    else:
        # is base type
        element_type = [text[0]]
        offset = 1

    # pointer.
    while text[offset] == '*':
        element_type.append(text[offset])
        offset += 1

    element_type = global_vars.parse_type(element_type, is_function_return_type, is_function_attr)

    # compensate for metadata offset
    offset += metadata_offset

    return element_type, offset


def parse_operand(text, is_typed = False):
    """
    Parses an operand and returns a corresponding dict with keys {'type', 'value', 'vector_type'}
    """

    logging.debug('Calling parse_operand({}, {})'.format(text, is_typed))

    if is_typed:
        operand_type, offset = extract_type(text)
        text = text[offset:]

    else:
        operand_type = None

    if text[0] == '%':
        # %val
        value = text[0]+text[1]
        retval = Value('virtual_reg', value, operand_type)
    
    elif text[0] == '@':
        # @name
        value = text[0]+text[1]
        retval = Value('global_var', value, operand_type)

    elif len(text) == 1:
        # 0.0 or 0.0e+00 or 0
        value = text[0]
        retval = Value('immediate', value, operand_type)
    
    elif text[0] == '!':
        # ! metadata
        
        # Empty DIExpression
        if text[1:4] == ['DIExpression', '(', ')']:
            retval = Value('metadata', 'empty', operand_type)

        elif text[1].isdigit():
            value = text[0]+text[1]
            retval = Value('metadata', value, operand_type)

        else:
            raise ParsingException('Metadata reference expected. {} given'.format(text))

        
    elif text[0] == '<':
        # vector type
        text = tools.split_into_sublist(text[1:-1], ',')
        
        # each pair is type value; they have the same type
        # so is sufficient to parse the type of the first element.
        # <i32 0, i32 1, ...>
        # NB: i can have <i32 0, i32 %x>
        
        value = []
        for operand in text:
            val = parse_operand(operand, True)
            value.append(val)

        retval = Value('vector', value, operand_type)
    
    elif text[0] == 'getelementptr':
        val = memory_operations.parse_getelementptr_operation(text, False)
        retval = Value('address', val, operand_type)

    elif text[0] in conversion_operations.conversion_operations:
        val = conversion_operations.parse_conversion_operation(text, False)
        retval = Value('conversion', val, operand_type)
        
    else:
        raise ParsingException('Operand not supported.\n{}'.format(text))

    return retval


def parse_int_specific_attr(text, operation_code):
    """
    Parses and removes integer specific attributes.
    It returns the list of found attributes.
    """

    logging.debug('Calling parse_int_specific_attr({}, {})'.format(text, operation_code))

    supported_op_code = ['add', 'sub', 'mul', 'shl']

    if operation_code not in supported_op_code:
        raise ParsingException('Binary operation "{}" not expected. {} only supported for integer specific attributes.\n{}'.format(operation_code, supported_op_code, text))
    
    # nuw: no unsigned wrap
    # nsw: no signed wrap
    specific_attributes = ['nuw', 'nsw']
    ret_attr = []

    for attr in specific_attributes:
        if attr in text:
            text.remove(attr)
            ret_attr.append(attr)

    return ret_attr, text


def parse_fp_specific_attr(text, operation_code):
    """
    Parses and removes floating point "fast-math flags" specific attributes.
    It returns the list of found attributes.
    """

    logging.debug('Calling parse_fp_specific_attr({}, {})'.format(text, operation_code))

    supported_op_code = ['fadd', 'fsub', 'fmul', 'fdiv', 'frem', 'fcmp', 'call']

    if operation_code not in supported_op_code:
        raise ParsingException('Binary operation "{}" not expected. {} only supported for floating point specific attributes.\n{}'.format(operation_code, supported_op_code, text))

    # just for optimizations, can be safely skipped in simulation
    fast_math_flags = ['nnan', 'ninf', 'nsz', 'arcp', 'contract', 'afn', 'reassoc', 'fast']

    ret_attr = []

    for attr in fast_math_flags:
        if attr in text:
            text.remove(attr)
            ret_attr.append(attr)

    return ret_attr, text


def parse_int_div_specific_attr(text, operation_code):
    """
    Parses and removes integer_division specific attributes.
    It returns the list of found attributes.
    """

    logging.debug('Calling parse_int_div_specific_attr({}, {})'.format(text, operation_code))

    supported_op_code = ['udiv', 'sdiv', 'lshr', 'ashr']

    if operation_code not in supported_op_code:
        raise ParsingException('Binary operation "{}" not expected. {} only supported for division specific attributes.\n{}'.format(operation_code, supported_op_code, text))

    specific_attributes = ['exact']

    ret_attr = []

    for attr in specific_attributes:
        if attr in text:
            text.remove(attr)
            ret_attr.append(attr)
    
    return ret_attr, text
