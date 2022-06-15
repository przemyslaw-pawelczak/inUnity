import logging

from ScEpTIC import tools
from ScEpTIC.AST.elements.instructions.memory_operations import AllocaOperation, LoadOperation, StoreOperation, GetElementPointerOperation
from ScEpTIC.exceptions import ParsingException, NotImplementedException
from ScEpTIC.llvmir_parser.sections_parser import global_vars

from . import binary_operations

def parse_memory_operation(text):
    """
    Parses and returns a memory operation.
        - alloca
        - load
        - getelementptr
        - store
    """

    logging.debug('Calling is_alloca_operation({})'.format(text))
    
    if is_memory_operation_with_return(text, 'alloca'):
        instruction_type = 'alloca'
        instruction_value = parse_alloca_operation(text)
        
    elif is_memory_operation_with_return(text, 'load'):
        instruction_type = 'load'
        instruction_value = parse_load_operation(text)

    elif is_memory_operation_with_return(text, 'getelementptr'):
        instruction_type = 'getelementptr'
        instruction_value = parse_getelementptr_operation(text)

    elif is_memory_operation_without_return(text, 'store'):
        instruction_type = 'store'
        instruction_value = parse_store_operation(text)
    else:
        return None

    if logging.getLogger().isEnabledFor(logging.DEBUG):
        logging.debug('Parsed {} instruction:\n{}'.format(instruction_type, instruction_value))

    return instruction_value


def is_memory_operation(text):
    """
    Return if an instruction is a memory operation.
    """

    logging.debug('Calling is_alloca_operation({})'.format(text))

    if len(text) < 4:
        return False

    # fence imposes instruction ordering
    # cmpoxchg compares modifies memory
    # atomicrmw atomically modifies memory
    not_implemented = ['fence', 'cmpxchg', 'atomicrmw']

    if text[0] in not_implemented or text[3] in not_implemented:
        raise NotImplementedException('Memory Operation "{}" not supported!'.format(text[3]))

    return is_memory_operation_with_return(text) or is_memory_operation_without_return(text)


def is_memory_operation_with_return(text, operation_code = None):
    """
    Return if an instruction is a memory operation with a return.
    """

    logging.debug('Calling is_memory_operation_with_return({}, {})'.format(text, operation_code))

    if len(text) < 4:
        return False

    supported_mem_ops = [
        'alloca',
        'load',
        'getelementptr'
    ]

    # operation code is on position 3
    # % ret_reg = CODE ...
    op_code = text[3]
    
    if operation_code is None:
        correct_op_code = op_code in supported_mem_ops

    else:
        correct_op_code = op_code == operation_code

    return correct_op_code and text[0] == '%' and text[2] == '='


def is_memory_operation_without_return(text, operation_code = None):
    """
    Return if an instruction is a memory operation without a return.
    """

    logging.debug('Calling is_memory_operation_without_return({}, {})'.format(text, operation_code))

    if len(text) < 4:
        return False

    supported_mem_ops = [
        'store'
    ]

    # operation code is on position 0
    # CODE ...
    op_code = text[0]
    
    if operation_code is None:
        correct_op_code = op_code in supported_mem_ops

    else:
        correct_op_code = op_code == operation_code

    return correct_op_code


def parse_alloca_operation(text):
    """
    Parses and returns an alloca operation.
    <result> = alloca [inalloca] <type> [, <ty> <NumElements>] [, align <alignment>] [, addrspace(<num>)]
    """

    logging.debug('Calling is_alloca_operation({})'.format(text))

    if not is_memory_operation_with_return(text, 'alloca'):
        raise ParsingException('Memory operation "alloca" expected.\n{} given.'.format(text))
    
    # retrieve where the result must be stored
    target, offset = binary_operations.parse_result_target(text)
    text = text[offset+1:]

    # split into groups
    text = tools.split_context_into_sublist(text, ',')

    # type is on the first group
    elem_type = global_vars.parse_type(text[0])
    elem_num = '1'
    # remove parsed group
    text = text[1:]

    # if present, the second group is the number of elements to be allocated.
    # Is represented as type elements. Only num elements needed, which is on pos. 1
    if text[0][0] not in ['align', 'addrspace']:
        elem_num = text[1][1]
        text = text[1:]

    # get the alignment
    align = None
    if text[0][0] == 'align':
        align = text[0][1]

    return AllocaOperation(target, elem_type, elem_num, align)


def parse_load_operation(text):
    """
    Parses and returns a load operation.
    <result> = load [volatile] <ty>, <ty>* <pointer>[, align <alignment>]
    <result> = load atomic [volatile] <ty>, <ty>* <pointer> [syncscope("<target-scope>")] <ordering>, align <alignment>
    """

    logging.debug('Calling parse_load_operation({})'.format(text))

    if not is_memory_operation_with_return(text, 'load'):
        raise ParsingException('Memory operation "load" expected.\n{} given.'.format(text))

    # retrieve where the result must be stored
    target, offset = binary_operations.parse_result_target(text)
    text = text[offset+1:]
    volatile = False

    # get if is marked as volatile
    if 'volatile' in text:
        volatile = True
        text.remove('volatile')

    if text[0] == 'atomic':
        # not a C feature
        raise NotImplementedException('Atomic loading not implemented!')
    
    # text[0] -> load type
    # text[1] -> type and pointer
    # text[2] -> if present, alignment
    text = tools.split_context_into_sublist(text, ',')
    
    load_type = global_vars.parse_type(text[0])
    element = binary_operations.parse_operand(text[1], True)

    if len(text) > 2:
        # align number
        align = text[2][1]

    else:
        align = None

    return LoadOperation(target, load_type, element, align, volatile)


def parse_store_operation(text):
    """
    Parses and returns a store operation.
    store [volatile] <ty> <value>, <ty>* <pointer>[, align <alignment>]
    store atomic [volatile] <ty> <value>, <ty>* <pointer> [syncscope("<target-scope>")] <ordering>, align <alignment>
    """

    logging.debug('Calling parse_store_operation({})'.format(text))

    if not is_memory_operation_without_return(text, 'store'):
        raise ParsingException('Memory operation "store" expected.\n{} given.'.format(text))

    volatile = False

    # get if is marked as volatile
    if 'volatile' in text:
        volatile = True
        text.remove('volatile')

    if text[1] == 'atomic':
        # not a C feature
        raise NotImplementedException('Atomic loading not implemented!')
    
    text = tools.split_context_into_sublist(text[1:], ',')

    store_value = binary_operations.parse_operand(text[0], True)
    
    store_target = binary_operations.parse_operand(text[1], True)
    
    # has alignment
    if len(text) > 2:
        # align value
        align = text[2][1]

    else:
        align = None

    return StoreOperation(store_target, store_value, align, volatile)


def parse_getelementptr_operation(text, has_target = True):
    """
    Parses and returns a getelementptr operation.
    <result> = getelementptr inbounds <ty>, <ty>* <ptrval>{, [inrange] <ty> <idx>}*
    """

    logging.debug('Calling parse_getelementptr_operation({}, {})'.format(text, has_target))

    if has_target and not is_memory_operation_with_return(text, 'getelementptr'):
        raise ParsingException('Memory operation "getelementptr" expected.\n{} given.'.format(text))
    
    if not has_target and not is_memory_operation_without_return(text, 'getelementptr'):
        raise ParsingException('Memory operation "getelementptr" expected.\n{} given.'.format(text))

    # retrieve where the result must be stored
    if has_target:
        target, offset = binary_operations.parse_result_target(text)
        text = text[offset+1:]

    else:
        text = tools.list_sanitize(text, '(')
        text = tools.list_sanitize(text, ')')
        text = text[1:]
        target = None

    inbounds = False

    # get if is marked as inbounds
    if 'inbounds' in text:
        inbounds = True
        text.remove('inbounds')

    # text[0]  -> type
    # text[1]  -> element
    # text[2:] -> indexes
    text = tools.split_context_into_sublist(text, ',')

    base_type = global_vars.parse_type(text[0])
    element = binary_operations.parse_operand(text[1], True)
    indexes = []

    # parse the indexes
    for index_pair in text[2:]:
        inrange = False
        
        if index_pair[0] == 'inrange':
            inrange = True
            index_pair = index_pair[1:]

        index = binary_operations.parse_operand(index_pair, True)
        # add inrange attribute
        index.inrange = inrange

        indexes.append(index)

    return GetElementPointerOperation(target, element, base_type, indexes, inbounds)
