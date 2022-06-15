import logging

from ScEpTIC import tools
from ScEpTIC.exceptions import ParsingException

from .sections_parser import headers
from .sections_parser import custom_types
from .sections_parser import global_vars
from .sections_parser import function
from .sections_parser import attributes_groups
from .sections_parser import metadata

def divide_into_sections(text, force_extraction = False):
    """
    Divides code into sections

    Document structure (in order):
        - Headers (source file name, target datalayout, target triple)
        - Custom Types (Struct and Union) Definitions
        - Global Variables Definitions
        - Function Definitions
        - Function's Attributes Definitions
        - Debug Informations
    """

    logging.debug('Calling divide_into_sections()')
    
    # verification functions to be called, in order.
    simple_elements_functions = [
        headers.is_header,
        custom_types.is_custom_type,
        global_vars.is_global_var_def,
        function.is_function_declaration,
        attributes_groups.is_attributes_group,
        metadata.is_metadata
    ]

    # name of the section extracted by the function
    section_names = [
        'headers',
        'custom_types',
        'global_vars',
        'function_declarations',
        'attributes_groups',
        'metadata'
    ]

    sections = dict.fromkeys(section_names, [])

    for i, f_reference in enumerate(simple_elements_functions):
        # extract elements
        section, text = simple_elements_extractor(text, f_reference)
        sections[section_names[i]] = section

    # special extraction
    sections['function_definitions'], text = function_def_elements_extractor(text)

    if len(text) > 0:
        logging.critical("Some code has not been persed!\n{}\n".format(tools.fancy_list_to_str(text)))

    return sections


def simple_elements_extractor(text, verification_function):
    """
    Extract the section composed by simple elements of the same type.
    An element is simple if its contained inside a single line of code.
    The type of the elements is given by the verification_function.
    It returns als the lines that have not been parsed.
    """

    logging.debug('Calling simple_elements_extractor()')

    lines = get_elements_lines(text, verification_function)
    
    elements = [text[line] for line in lines]

    text = remove_lines(text, lines)

    # fancy logging
    if logging.getLogger().isEnabledFor(logging.INFO):
        elements_str = tools.fancy_list_to_str(elements)

        logging.info('Elements extracted with {}.{}()\n{}\n'.format(verification_function.__module__, verification_function.__name__, elements_str))

    return elements, text


def function_def_elements_extractor(text):
    """
    Extract the function_definition section (both definition and body).
    Acts like simple_elements_extractor, but only extracts function defs.
    """

    logging.debug('Calling function_def_elements_extractor()')

    lines = get_elements_lines(text, function.is_function_definition)

    elements = []

    for line in lines:
        body, relative_body_end = extract_function_body(text[line:])
        
        element = {'def': text[line], 'body': body}
        elements.append(element)

        # definition line already parsed. body lines start from next one.
        line = line + 1
        
        # cast range to list to fix python3 compatibility issues
        rng = list(range(line, line+relative_body_end))
        
        # append body lines to parsed lines
        lines = lines + rng

    text = remove_lines(text, lines)

    # fancy logging
    if logging.getLogger().isEnabledFor(logging.INFO):
        elements_log_str = ""
        
        max_id = len(elements)
        spacing = len(str(max_id))
        # leading 0
        id_format = '{:0'+str(spacing)+'}'
        # add space for ': ['
        body_spacing = ' '*(spacing+2)

        # line number: line content
        #              body line number: body content
        for i in range(0, max_id):
            # format line number
            line_num = id_format.format(i)

            # format line with max length default
            elements_log_str += tools.instert_new_line_every("{}: {}\n".format(line_num, elements[i]['def']), new_line_padding=' '*(spacing+2))
            
            # format function body
            elements_log_str += tools.fancy_list_to_str(elements[i]['body'], body_spacing)
            elements_log_str += "\n"

        logging.info('Elements extracted with {}.{}()\n{}'.format(function.is_function_definition.__module__, function.is_function_definition.__name__, elements_log_str))

    return elements, text


def extract_function_body(text):
    """
    Extracts and returns the function body.
    Returns also the number of the latest parsed line.
    """

    logging.debug('Calling extract_function_body()')

    if text[0][-1] != '{':
        raise ParsingException('Unable to find function body initial delimiter "{".\n'+"{}".format(text))

    try:
        body_start = 1
        # find the line composed by only the body final delimiter
        # NB: is a relative value w.r.t. the function definition line
        body_end = text.index(['}'])
    except ValueError:
        raise ParsingException('Unable to find function body final delimiter "}".\n'+"{}".format(text))

    return text[body_start:body_end], body_end


def get_elements_lines(text, verification_function):
    """
    Returns the line number of the elements on which verification_function returns true.
    """

    logging.debug('Calling get_elements_lines()')

    lines = []

    for i, val in enumerate(text):
        
        if verification_function(val):
            lines.append(i)

    return lines


def remove_lines(text, lines):
    """
    Removes lines that have already been parsed.
    """

    logging.debug('Calling remove_lines()')
    
    if lines is None:
        return text

    # remove duplicates and revert back to list
    lines = list(set(lines))
    lines.sort()

    # compensation value: if line 1 gets removed, line 2 becomes new line 1.
    # on remove add 1 to compensation
    compensation = 0

    for i in lines:
        del text[i-compensation]
        compensation += 1

    return text
