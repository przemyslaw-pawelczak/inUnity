import logging

from ScEpTIC import tools
from ScEpTIC.AST.elements.instructions.other_operations import CompareOperation, PhiOperation, SelectOperation, CallOperation, VaArgOperation
from ScEpTIC.emulator.intermittent_executor import profiling
from ScEpTIC.exceptions import ParsingException, LLVMSyntaxErrorException, NotImplementedException
from ScEpTIC.llvmir_parser.sections_parser import function
from ScEpTIC.llvmir_parser.sections_parser import global_vars

from . import binary_operations


def parse_other_operation(text):
    """
    Parses and return the other operations, which are:
        - icmp, fcmp
        - phi
        - select
        - va_arg
        - call
    """

    logging.debug('Calling parse_other_operation({})'.format(text))

    if not is_other_operation(text):
        raise ParsingException('Other operation (icmp, fcmp, phi) expected.\n{} given'.format(text))

    instruction_type = None

    if is_other_operation(text, 'cmp'):
        instruction_type = 'cmp'
        instruction_value = parse_cmp_operation(text)

    elif is_other_operation(text, 'phi'):
        instruction_type = 'phi'
        instruction_value = parse_phi_operation(text)

    elif is_other_operation(text, 'select'):
        instruction_type = 'select'
        instruction_value = parse_select_operation(text)

    elif is_other_operation(text, 'va_arg'):
        instruction_type = 'va_arg'
        instruction_value = parse_va_arg_instruction(text)

    elif is_call_instruction(text):
        instruction_type = 'call'
        instruction_value = parse_call_instruction(text)

    if logging.getLogger().isEnabledFor(logging.DEBUG):
        logging.debug('Parsed {} instruction:\n{}'.format(instruction_type, instruction_value))
        
    return instruction_value


def is_other_operation(text, operation_code = None):
    """
    Returns if a given instruction is is an icmp or fcmp operation.
    """

    logging.debug('Calling is_other_operation({}, {})'.format(text, operation_code))

    if len(text) < 4:
        return False

    not_supported_ops = ['landingpad', 'catchpad', 'cleanuppad']

    op_code = text[3]
    
    if text[0] in not_supported_ops or op_code in not_supported_ops:
        raise NotImplementedException('Operation {} not implemented!'.format(op_code))

    if operation_code is None:
        valid_op = op_code in ['icmp', 'fcmp', 'phi', 'select', 'call', 'va_arg']
        is_call = is_call_instruction(text)

    elif operation_code == 'cmp':
        valid_op = op_code in ['icmp', 'fcmp']
        is_call = False

    else:
        valid_op = op_code == operation_code
        is_call = False

    return (valid_op and text[0] == '%' and text[2] == '=') or is_call


def is_call_instruction(text):
    """
    Returns if a given instruction is is a call one.
    """

    logging.debug('Calling is_call_instruction({})'.format(text))

    if len(text) < 5:
        return False

    token = 'call'

    # can be:
    # call ...
    # tail call
    # % x = call
    # % x = tail call
    return token in text[:5]


def parse_cmp_operation(text):
    """
    Parses and returns an icmp/fcmp operation.
    <result> = icmp <cond> <ty> <op1>, <op2>
    <result> = fcmp [fast-math flags]* <cond> <ty> <op1>, <op2>
    """

    logging.debug('Calling parse_cmp_operation({})'.format(text))

    if not is_other_operation(text, 'cmp'):
        raise ParsingException('Cmp operation (icmp, fcmp) expected.\n{} given.'.format(text))

    # retrieve where the result must be stored
    target, offset = binary_operations.parse_result_target(text)
    operation_code = text[offset]
    text = text[offset+1:]
    
    # fcmp can have fast-math flags
    # but can be ignored. just parse them
    if operation_code == 'fcmp':
        specific_attr, text = binary_operations.parse_fp_specific_attr(text, 'fcmp')

    # parse condition, type and operands
    parsed = parse_cond_type_operands(text, operation_code)
    comparation_type = 'int' if operation_code == 'icmp' else 'float'

    return CompareOperation(target, parsed['op1'], parsed['op2'], parsed['condition'], comparation_type, operation_code)


def parse_cond_type_operands(text, operation_code):
    """
    Parses and returns the condition, the type and the operands of an operation as a dict
    with keys {'op1', 'op2', 'condition'}
    If the condition is not a valid one, it raises an exception.
    """

    logging.debug('Calling parse_cond_type_operands({}, {})'.format(text, operation_code))

    # condition is always at offset 0
    cond = text[0]

    if not is_valid_cond(cond, operation_code):
        raise ParsingException('Condition {} not valid for {} operation.'.format(cond, operation_code))

    # parse type and operands.
    retval = binary_operations.parse_type_and_operands(text[1:])
    retval['condition'] = cond

    return retval


def is_valid_cond(cond, operation_code):
    """
    Returns if a given condition is a valid one for a given operation.
    """

    logging.debug('Calling is_valid_cond({}, {})'.format(cond, operation_code))

    if operation_code == 'icmp':
        valid_conds = ['eq', 'ne', 'ugt', 'uge', 'ult', 'ule', 'sgt', 'sge', 'slt', 'sle']
    elif operation_code == 'fcmp':
        valid_conds = ['false', 'oeq', 'ogt', 'oge', 'olt', 'ole', 'one', 'ord', 'ueq', 'ugt', 'uge', 'ult', 'ule', 'une', 'uno', 'true']

    return cond in valid_conds


def parse_phi_operation(text):
    """
    Parses and returns a phi operation.
    <result> = phi <ty> [ <val0>, <label0>], ...
    """

    logging.debug('Calling parse_phi_operation({})'.format(text))

    if not is_other_operation(text, 'phi'):
        raise ParsingException('phi operation expected.\n{} given.'.format(text))

    # retrieve where the result must be stored
    target, offset = binary_operations.parse_result_target(text)
    text = text[offset+1:]

    # get type. it is after 'phi' and before the first [
    index = text.index('[')
    return_type = global_vars.parse_type(text[:index])

    # split values
    text = tools.split_context_into_sublist(text[index:], ',')
    
    values = {}

    # pair:   value, %label
    for pair in text:
        # 1 to remove '['
        # -4 to remove [',', '%', 'label', ']']
        value = binary_operations.parse_operand(pair[1:-4])
        
        # -3 to start from '%'
        # -1 to end before ']'
        label = tools.list_to_string(pair[-3:-1])
        
        values[label] = value

    return PhiOperation(target, return_type, values)


def parse_select_operation(text):
    """
    Parses a select operation.
    <result> = select selty <cond>, <ty> <val1>, <ty> <val2>
    """

    logging.debug('Calling parse_select_operation({})'.format(text))

    if not is_other_operation(text, 'select'):
        raise ParsingException('select operation expected.\n{} given.'.format(text))

    # retrieve where the result must be stored
    target, offset = binary_operations.parse_result_target(text)
    text = text[offset+1:]

    # get a list of 3 sublists:
    # 0: selty <cond>
    # 1: <ty> <val1>
    # 2: <ty> <val2>
    elements = tools.split_context_into_sublist(text, ',')

    # parse selection type and conditional
    cond = binary_operations.parse_operand(elements[0], True)

    # parse value list 1
    el1 = binary_operations.parse_operand(elements[1], True)

    # parse value list 2
    el2 = binary_operations.parse_operand(elements[2], True)

    return SelectOperation(target, cond, el1, el2)


def parse_call_instruction(text):
    """
    Parses and returns a call instruction.
    <result> = [tail | musttail | notail ] call [fast-math flags] [cconv] [ret attrs] <ty>|<fnty> <fnptrval>(<function args>) [fn attrs]
                 [ operand bundles ]
    """

    logging.debug('Calling parse_call_instruction({})'.format(text))
    
    if not is_call_instruction(text):
        raise ParsingException('call instruction expected.\n{} given.'.format(text))

    text = profiling.pre_parse_profiling_log(text, '@')

    target = None

    # has target
    if text[2] == '=':
        target, offset = binary_operations.parse_result_target(text)
        text = text[offset:]

    # parse and remove fast-math flags and tail attributes
    fp_attr, text = binary_operations.parse_fp_specific_attr(text, 'call')
    tail_attr, text = parse_tail_specific_attr(text)

    # first element is call, remove it.
    text = text[1:]

    # parse and remove calling convetion
    cc_attr, text = parse_calling_convention(text)

    # parse and remove ret attrs
    ret_attr, text = parse_return_parameter_attr(text)

    # parse <ty>
    return_type, offset = binary_operations.extract_type(text, True)
    text = text[offset:]

    function_signature = []

    # parse <fnty> for var_args
    if text[0] == '(':
        index = tools.get_index_of_closed_par(text, '(', ')')
        function_signature = function.parse_function_arguments(text[1:index])
        text = text[index+1:]

    if text[0] == 'bitcast':
        index_name = text.index('@')
        index_arg_open = tools.list_rindex(text, '(')
        text = text[index_name:index_name+2] + text[index_arg_open:]

    if text[0] != '@':
        raise LLVMSyntaxErrorException('Function identifier must start with @. {} given.\n{}'.format(text[0], text))

    function_name = text[0]+text[1]
    
    # remove ['@', 'function_name']
    text = text[2:]
    index = tools.get_index_of_closed_par(text, '(', ')')

    # parse arguments passed to the function
    function_args_lst = tools.split_context_into_sublist(text[1:index], ',')
    function_args = []
    
    for arg in function_args_lst:
        # improper usage of function extract_type_and_attributes: in this case divides type and value from attributes
        arg, attributes = function.extract_type_and_attributes(arg)

        arg_val = binary_operations.parse_operand(arg, True)
        arg_val.attributes = attributes

        function_args.append(arg_val)

    text = text[index+1:]

    # TO BE PARSED HERE (for future updates): fn attrs, operand bundles

    attrs = {'fp_math': fp_attr, 'tail': tail_attr, 'cc': cc_attr, 'return': ret_attr}

    return CallOperation(target, function_name, return_type, function_signature, function_args, attrs)


def parse_tail_specific_attr(text):
    """
    Parses and removes tail attributes of call instruction.
    They are not useful in my analysis (used just for optimization)
    """

    logging.debug('Calling parse_tail_specific_attr({})'.format(text))

    tail_tokens = ['tail', 'musttail', 'notail']

    ret = []

    while text[0] in tail_tokens:
        ret.append(text[0])
        text = text[1:]

    return ret, text


def parse_calling_convention(text):
    """
    Parses and removes calling conventions attributes of call instruction.
    """

    logging.debug('Calling parse_calling_convention({})'.format(text))

    ccs_tokens = ['ccc', 'fastcc', 'coldcc', 'webkit_jscc', 'anyregcc', 'preserve_mostcc', 'preserve_allcc', 'cxx_fast_tlscc', 'swiftcc']

    calling_conventions = []

    while text[0] in ccs_tokens:
        calling_conventions.append(text[0])
        text = text[1:]

    # cc <n>
    if text[0] == 'cc' and text[1].isdigit():
        calling_conventions.append(text[0]+text[1])
        text = text[2:]

    return calling_conventions, text


def parse_return_parameter_attr(text):
    """
    Parses and removes return attributes of call instruction.
    """

    logging.debug('Calling parse_return_parameter_attr({})'.format(text))

    param_attr = ['zeroext', 'signext', 'inreg', 'byval', 'inalloca', 'sret', 'noalias', 'nocapture', 'nest', 'returned', 'nonnull', 'swiftself', 'swifterror']

    ret_param_attr = []

    while text[0] in param_attr:
        ret_param_attr.append(text[0])
        text = text[1:]

    return ret_param_attr, text


def parse_va_arg_instruction(text):
    """
    Parses a va_arg instruction and returns it.
    Note: THIS IS NOT FULLY SUPPORTED BY LLVM CODE GENERATOR ON MANY TARGETS

    <resultval> = va_arg <va_list*> <arglist>, <argty>
    %tmp = va_arg i8* %ap2, i32
    It returns a value of the specified argument type and increments the va_list to point to the next argument. The actual type of va_list is target specific.
    """

    logging.debug('Calling parse_va_arg_instruction({})'.format(text))

    if not is_other_operation(text, 'va_arg'):
        raise ParsingException('va_arg instruction expected.\n{} given.'.format(text))

    # parse target and remove <resultval> = va_arg
    target, offset = binary_operations.parse_result_target(text)
    text = text[offset+1:]

    # split variable argument list and argument type
    text = tools.split_context_into_sublist(text, ',')

    # first group is the list virtual register
    list_element = binary_operations.parse_operand(text[0], True)

    # second group is the type of each element in the list
    arg_type = global_vars.parse_type(text[1])

    return VaArgOperation(target, list_element, arg_type)
