import logging

from ScEpTIC import tools
from ScEpTIC.exceptions import ParsingException
from ScEpTIC.llvmir_parser.token_generator import TOKEN_SPACE


def parse_header_section(text, log_section_content = False):
    """
    Parses the header section and returns a dictionary containing parsed values
    """

    logging.debug('Calling parse_header_section({}, {})'.format(text, log_section_content))
    
    headers = {}

    for line in text:
        if is_source_file_name(line):
            headers['source_filename'] = get_source_file_name(line)
            
        elif is_target_datalayout(line):
            headers['target_datalayout'] = get_target_datalayout(line)

        elif is_target_triple(line):
            headers['target_triple'] = get_target_triple(line)

    if len(headers) < 3:
        logging.warning('Some headers are missing!')

    if logging.getLogger().isEnabledFor(logging.INFO):
        log_str = 'Parsed header section. {} headers found'.format(len(headers))

        if log_section_content:
            log_str += ':\n{}'.format(tools.fancy_dict_to_str(headers))

        else:
            log_str += '.\n{}'.format(tools.fancy_dict_keys_to_str(headers))

        logging.info(log_str)

    return headers


def get_source_file_name(text):
    """
    Parses a line containing the source file name and returns it
    """

    logging.debug('Calling get_source_file_name({})'.format(text))

    if not is_source_file_name(text):
        raise ParsingException('Invalid file format! Line #2 must start with source_filename')

    start, end = tools.get_list_apex_boundaries(text)
    source_filename = tools.list_to_string(text[start:end], {TOKEN_SPACE: ' '})
        
    logging.debug("source_filename: {}".format(source_filename))
        
    return source_filename


def is_source_file_name(text):
    """
    Return if parsed line represents source_filename
    """

    logging.debug('Calling is_source_file_name({})'.format(text))

    return isinstance(text, list) and len(text) > 1 and text[0] == 'source_filename'


def get_target_datalayout(text):
    """
    Parses a line containing the target datalayout and returns its elements
    """

    logging.debug('Calling get_target_datalayout({})'.format(text))

    if not is_target_datalayout(text):
        raise ParsingException('Invalid file format! Line #3 must start with target datalayout')

    start, end = tools.get_list_apex_boundaries(text)
    target_datalayout = tools.list_join(text[start:end]).split('-')

    logging.debug("target_datalayout: {}".format(target_datalayout))
    
    return target_datalayout


def is_target_datalayout(text):
    """
    Return if parsed line represents target_datalayout
    """

    logging.debug('Calling is_target_datalayout({})'.format(text))

    return isinstance(text, list) and len(text) > 2 and text[0] == 'target' and text[1] == 'datalayout'


def get_target_triple(text):
    """
    Parses a line containing the target triple / architecture and returns it
    """

    logging.debug('Calling get_target_triple({})'.format(text))

    if not is_target_triple(text):
        raise ParsingException('Invalid file format! Line #4 must start with target triple')

    start, end = tools.get_list_apex_boundaries(text)
    target_triple = tools.list_join(text[start:end])

    logging.debug("target_triple: {}".format(target_triple))

    return target_triple


def is_target_triple(text):
    """
    Return if parsed line represents target_triple
    """

    logging.debug('Calling is_target_triple({})'.format(text))

    return isinstance(text, list) and len(text) > 2 and text[0] == 'target' and text[1] == 'triple'


def is_header_section(text):
    """
    Return if the first 3 lines represents the headers
    """

    logging.debug('Calling is_header_section({})'.format(text))

    return isinstance(text, list) and len(text) > 2 and is_source_file_name(text[0]) and is_target_datalayout(text[1]) and is_target_triple(text[2])


def is_header(text):
    """
    Return if the line represents an header
    """

    logging.debug('Calling is_header({})'.format(text))

    return is_source_file_name(text) or is_target_datalayout(text) or is_target_triple(text)
