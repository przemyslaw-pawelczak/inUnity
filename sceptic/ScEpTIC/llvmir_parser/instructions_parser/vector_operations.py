import logging

from ScEpTIC.exceptions import ParsingException, NotImplementedException


def parse_vector_operation(text):
    """
    Parses a vector operation.
    They are not available in C language, so are not supported for my simulation.
    """

    logging.debug('Calling parse_vector_operation({})'.format(text))

    if not is_vector_operation(text):
        raise ParsingException('Vector operation (extractelement, insertelement, shufflevector) expected.\n{} given'.format(text))

    raise NotImplementedException('Vector operations are not supported!')


def is_vector_operation(text):
    """
    Returns if a given instruction is a vector operation.
    """

    logging.debug('Calling is_vector_operation({})'.format(text))

    if len(text) < 4:
        return False

    vector_ops = ['extractelement', 'insertelement', 'shufflevector']

    op_code = text[3]

    correct_op_code = op_code in vector_ops

    return correct_op_code and text[0] == '%' and text[2] == '='
