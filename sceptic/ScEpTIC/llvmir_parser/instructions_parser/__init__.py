import logging

from ScEpTIC.exceptions import ParsingException
from ScEpTIC.llvmir_parser.sections_parser import metadata

from . import aggregate_operations
from . import binary_operations
from . import conversion_operations
from . import memory_operations
from . import other_operations
from . import terminator_instructions
from . import vector_operations


def parse_instruction(text, line_number, function_name):
    """
    Parses and returns an instruction

    Types of instructions:
        - Terminator Instructions
        - Binary Operations
        - Bitwise Binary Operations
        - Vector Operations
        - Aggregate Operations
        - Memory Access and Addressing Operations
        - Conversion Operations
        - Other Operations
    """

    instruction_metadata, index = metadata.get_element_metadata(text, 'line #{} of {}'.format(line_number, function_name), True)
    
    retval = None

    if index > 0:
        text = text[:index]

    if terminator_instructions.is_terminator_instruction(text):
        retval = terminator_instructions.parse_terminator_instruction(text)

    elif binary_operations.is_binary_operation(text):
        retval = binary_operations.parse_binary_operation(text)

    elif vector_operations.is_vector_operation(text):
        retval = vector_operations.parse_vector_operation(text)

    elif aggregate_operations.is_aggregate_operation(text):
        retval = aggregate_operations.parse_aggregate_operation(text)
        
    elif memory_operations.is_memory_operation(text):
        retval = memory_operations.parse_memory_operation(text)

    elif conversion_operations.is_conversion_operation(text):
        retval = conversion_operations.parse_conversion_operation(text)

    elif other_operations.is_other_operation(text):
        retval = other_operations.parse_other_operation(text)

    else:
        raise ParsingException('Unable to process instruction on line #{} of {}\n{}'.format(line_number, function_name, text))

    # unreachable instruction returns None
    if retval is None:
        return None

    retval.metadata = instruction_metadata

    logging.info('Parsed operation: {}'.format(retval))

    return retval
