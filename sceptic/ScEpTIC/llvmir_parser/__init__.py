from . import token_generator
from . import sections_divider
from . import sections_parser

import logging

def parse_file(file, set_logging_level = None, log_section_content = False):
    """
    Parses a .ll file and returns the AST
    """

    logging.debug('Calling parse_file()')

    current_logging_level = logging.getLogger().level

    if set_logging_level is not None:
        logging.getLogger().setLevel(set_logging_level)

    # parse file to get corresponding tokens
    tokens = token_generator.get_symbols_from_file(file)

    # divide into section
    sections = sections_divider.divide_into_sections(tokens)

    # parse each section
    parsed_sections = sections_parser.parse_sections(sections, log_section_content)

    if set_logging_level is not None:
        logging.getLogger().setLevel(current_logging_level)


    return parsed_sections
