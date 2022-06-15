import logging

from ScEpTIC import tools
from ScEpTIC.AST.elements.instructions.termination_instructions import ReturnOperation, BranchOperation, SwitchOperation
from ScEpTIC.AST.elements.value import Value
from ScEpTIC.exceptions import ParsingException, NotImplementedException, LLVMSyntaxErrorException
from ScEpTIC.llvmir_parser.sections_parser import global_vars
from ScEpTIC.llvmir_parser.token_generator import SWITCH_NEW_LINE_MARKER

from . import binary_operations


def parse_terminator_instruction(text):
    """
    Parses and returns a terminator instruction.
    Terminator instructions:
        - ret:
        - br
        - switch:
    """

    logging.debug('Calling parse_terminator_instruction({})'.format(text))
    
    instruction_type = None

    if is_ret_instruction(text):
        instruction_type  = 'return'
        instruction_value = parse_ret_instruction(text)

    elif is_switch_instruction(text):
        instruction_type  = 'switch'
        instruction_value = parse_switch_instruction(text)

    elif is_branch_instruction(text):
        instruction_type  = 'branch'
        instruction_value = parse_branch_instruction(text)

    elif is_unreachable_instruction(text):
        instruction_type = 'unreachable'
        instruction_value = parse_unreachable_instruction(text)

    if logging.getLogger().isEnabledFor(logging.DEBUG):
        logging.debug('Parsed {} instruction:\n{}'.format(instruction_type, instruction_value))
    
    if instruction_type is None:
        raise ParsingException('Terminator instruction expected (ret, br or switch).\n{} given.'.format(text))

    return instruction_value


def is_terminator_instruction(text):
    """
    Returns if an instruction is a terminator instruction.
    """

    logging.debug('Calling is_terminator_instruction({})'.format(text))

    # not used in C
    not_implemented = ['indirectbr', 'invoke', 'resume', 'catchswitch', 'catchret', 'cleanupret']

    implemented = ['ret', 'br', 'switch', 'unreachable']

    # in terminator operations, operation type is always in position 0
    operation_type = text[0]
    
    if operation_type in not_implemented:
        raise NotImplementedException('Terminator Instruction "{}" not implemented!'.format(operation_type))

    return operation_type in implemented


def is_ret_instruction(text):
    """
    Returns if an instruction is a retturn.
    """

    logging.debug('Calling is_ret_instruction({})'.format(text))

    return text[0] == 'ret'


def is_unreachable_instruction(text):
    """
    Returns if an instruction is an unreachable.
    """

    logging.debug('Calling is_unreachable_instruction({})'.format(text))

    return text[0] == 'unreachable'


def parse_ret_instruction(text):
    """
    Parses and returns a ret instruction.
    """

    logging.debug('Calling parse_ret_instruction({})'.format(text))

    if not is_ret_instruction(text):
        raise ParsingException('Terminator Instruction "ret" expected. {} given'.format(text))

    text = text[1:]
    
    if text[0] == 'void':
        retval = Value('immediate', None, global_vars.parse_type('void', True, True))
    else:
        retval = binary_operations.parse_operand(text, True)

    return ReturnOperation(retval)


def is_branch_instruction(text):
    """
    Returns if an instruction is a branch.
    """

    logging.debug('Calling is_br_instruction({})'.format(text))

    return text[0] == 'br'


def parse_unreachable_instruction(text):
    """
    Parses and returns an unreachable instruction.
    """

    logging.debug('Calling parse_unreachable_instruction({})'.format(text))

    return None


def parse_branch_instruction(text):
    """
    Parses and returns a branch instruction.
    """

    logging.debug('Calling parse_branch_instruction({})'.format(text))

    if not is_branch_instruction(text):
        raise ParsingException('Terminator Instruction "br" expected. {} given'.format(text))

    if is_conditional_branch_instruction(text):
        retval = parse_conditional_branch_instruction(text)

    elif is_unconditional_branch_instruction(text):
        retval = parse_unconditional_branch_instruction(text)

    else:
        raise ParsingException('Unable to identify branch operation: {}'.format(text))

    return retval


def is_unconditional_branch_instruction(text):
    """
    Returns if an instruction is an uncoditional branch.
    """

    logging.debug('Calling is_unconditional_branch_instruction({})'.format(text))

    return text[0] == 'br' and text[1] == 'label' and text[2] == '%'


def is_conditional_branch_instruction(text):
    """
    Returns if an instruction is a conditional branch.
    """

    logging.debug('Calling is_conditional_branch_instruction({})'.format(text))

    return text[0] == 'br' and text[1] == 'i1'


def parse_unconditional_branch_instruction(text):
    """
    Parses and returns an unconditional branch.

    br label <target>
    """

    logging.debug('Calling parse_unconditional_branch_instruction({})'.format(text))

    if not is_unconditional_branch_instruction(text):
        raise ParsingException('Unconditional Branch Instruction expected. {} given'.format(text))

    if text[2] != '%':
        raise LLVMSyntaxErrorException('Wrong label delimiter "{}". % expected.\n{}'.format(text[2], text))

    # target on element 3
    target = text[2]+text[3]

    return BranchOperation(None, target, None)


def parse_conditional_branch_instruction(text):
    """
    Parses and returns a conditional branch.
    br i1 <cond>, label <iftrue>, label <iffalse>
    """

    logging.debug('Calling parse_conditional_branch_instruction({})'.format(text))

    if not is_conditional_branch_instruction(text):
        raise ParsingException('Conditional Branch Instruction expected. {} given'.format(text))

    if text[2] != '%':
        raise LLVMSyntaxErrorException('Wrong condition delimiter "{}". % expected.\n{}'.format(text[2], text))

    # condition on element 3
    condition = binary_operations.parse_operand(text[2:4])
    
    true_index = text.index('label')+1
    true_label = tools.list_join(text[true_index:true_index+2])

    false_index = text.index('label', true_index) + 1
    false_label = tools.list_join(text[false_index:false_index+2])

    return BranchOperation(condition, true_label, false_label)


def is_switch_instruction(text):
    """
    Returns if an instruction is a switch
    """

    logging.debug('Calling is_switch_instruction({})'.format(text))

    return text[0] == 'switch' and '[' in text and ']' in text


def parse_switch_instruction(text):
    """
    Parses and returns a switch instruction.
    switch <intty> <value>, label <defaultdest> [ <intty> <val>, label <dest> ... ]
    switch i32 %val, label %otherwise [ i32 0, label %onzero i32 1, label %onone i32 2, label %ontwo ]
    """

    logging.debug('Calling parse_switch_instruction({})'.format(text))

    if not is_switch_instruction(text):
        raise ParsingException('Switch Instruction expected. {} given'.format(text))

    # switch i32 %var,
    # get type and element
    first_comma = tools.get_index_in_context(text, ',')
    element = binary_operations.parse_operand(text[1:first_comma], True)

    text = text[first_comma+1:]

    if text[0] != 'label':
        raise LLVMSyntaxErrorException('Default label declaration in Switch Instruction expected. "{}" given.\n{}'.format(text[first_comma+1], text))

    # get default label
    default_label = text[1]+text[2]

    # get switch values and split them into a list
    switch_start, switch_end = tools.get_list_boundaries(text, '[', ']')
    switch_elements = tools.split_into_sublist(text[switch_start:switch_end], SWITCH_NEW_LINE_MARKER)

    switch_pairs = []
    
    # switch pair example: i32 0, label %10
    for switch_pair in switch_elements:
        switch_pair = tools.split_into_sublist(switch_pair, ',')

        value = binary_operations.parse_operand(switch_pair[0], True)
        
        label = tools.list_join(switch_pair[1][1:])
        
        value.label = label
        
        switch_pairs.append(value)

    return SwitchOperation(element, default_label, switch_pairs)
