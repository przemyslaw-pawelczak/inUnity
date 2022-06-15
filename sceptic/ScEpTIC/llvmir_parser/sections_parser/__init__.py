import logging

from ScEpTIC.exceptions import ParsingException

from . import headers
from . import custom_types
from . import global_vars
from . import function
from . import attributes_groups
from . import metadata

def parse_sections(sections, log_section_content = False):
    """
    Parses all the sections using section parsers from the other components.
    It returns a dict containing the parsed values
    """

    logging.debug('Calling parse_sections()')
    
    # Names of the sections
    sections_names = [
        'headers',
        'custom_types',
        'global_vars',
        'function_declarations',
        'function_definitions',
        'attributes_groups',
        'metadata'
    ]
    
    # Functions that parses the corrisponding section name
    parsing_functions = [
        headers.parse_header_section,
        custom_types.parse_custom_types_section,
        global_vars.parse_global_vars_section,
        function.parse_function_declarations_section,
        function.parse_function_definition_section,
        attributes_groups.parse_attributes_groups_section,
        metadata.parse_metadata_section
    ]

    # check if all sections are present.
    not_present = ""

    for i in sections_names:
        if i not in sections:
            not_present = not_present + (i if len(not_present) == 0 else ', {}'.format(i))
    
    if len(not_present) > 0:
        raise ParsingException('The following sections have not been found: {}'.format(not_present))

    parsed_sections = {}

    for i in range(0, len(sections_names)):
        # get section name
        section_name = sections_names[i]

        # parse section using corresponding parser
        parsed_sections[section_name] = parsing_functions[i](sections[section_name], log_section_content)

    return parsed_sections
