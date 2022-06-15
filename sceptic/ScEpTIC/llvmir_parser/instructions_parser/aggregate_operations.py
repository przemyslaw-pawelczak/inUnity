import logging

from ScEpTIC.exceptions import ParsingException, NotImplementedException

def parse_aggregate_operation(text):
    """
    Parses an aggregate operation.
    They are not available in C language, so are not supported for the simulation.
    """

    logging.debug('Calling parse_aggregate_operation({})'.format(text))

    if not is_aggregate_operation(text):
        raise ParsingException('Aggregate operation (extractvalue, insertvalue) expected.\n{} given'.format(text))

    raise NotImplementedException('Aggregate operations are not supported!')


def is_aggregate_operation(text):
    """
    Returns if a given instruction is an aggregate operation.
    """

    logging.debug('Calling is_aggregate_operation({})'.format(text))

    if len(text) < 4:
        return False

    aggregate_ops = ['extractvalue', 'insertvalue']

    op_code = text[3]

    correct_op_code = op_code in aggregate_ops

    return correct_op_code and text[0] == '%' and text[2] == '='
