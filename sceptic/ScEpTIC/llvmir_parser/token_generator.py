import logging
import os.path
import re

from ScEpTIC import tools
from ScEpTIC.exceptions import ParsingException


TOKEN_SPACE = '{space}'
SWITCH_NEW_LINE_MARKER = '{SWITCH_NEW_LINE}'

COMMENT_TOKEN = ';'

# offset, element
ADMITTED_COMMENTS = {2: 'label'}

LLVM_FUNCTIONS_BLACKLIST = ['@llvm.objectsize.i64.p0i8', '@__memset_chk']

def get_symbols_from_file(file):
    """
    Returns a list of lines.
    Each line is represented as a list of different recognizable tokens
    """

    logging.debug("Calling get_symbols_from_file()")

    if not os.path.isfile(file):
        raise ParsingException("File {} not found!".format(file))
    
    file_content = []

    with open(file, 'r') as fp:
        for line in fp:

            ignore_line = False
            for element in LLVM_FUNCTIONS_BLACKLIST:
                if element in line:
                    ignore_line = True
                    break

            if ignore_line:
                continue

            parsed_line = get_symbols_from_line(line)
            parsed_line = remove_comment_from_line(parsed_line)

            # each line is an array of symbols
            if len(parsed_line) > 0:
                file_content.append(parsed_line)

    file_content = collapse_switch_statement(file_content)
    # fancy logging
    if logging.getLogger().isEnabledFor(logging.INFO):
        
        logging.info('Parsed file:\n{}\n\n'.format(tools.fancy_list_to_str(file_content)))

    return file_content


def get_symbols_from_line(line):
    """
    Return a list of symbols
    """

    logging.debug("Calling get_symbols_from_line()")
    parsed_line = []

    # replaces multiple subsequent line separators with a single space
    # \t\n\r\f\v
    sanitized_line = re.sub('(\s+)', ' ', line).split(' ')

    for element in sanitized_line:
        # split the line into words
        # + is to concatenate tokens like ['0.00e', '+', '00'] into ['0.00e+00']
        element = re.split('([^a-zA-Z0-9_\-\.\+]+)', element)

        for symbol in element:
            # split two symbols recognized as a single word
            # e.g. ),
            sym = re.split('([^!a-zA-Z0-9_\-\.\+])', symbol)

            for data in [x for x in sym if x]:
                parsed_line.append(data)

        # fix for joining
        if len(parsed_line) > 0:
            parsed_line.append(TOKEN_SPACE)
    
    if len(parsed_line) > 0:
        parsed_line = remove_unrelevant_spaces(parsed_line)
    
    return parsed_line


def remove_comment_from_line(line):
    """
    Removes comments from a line
    """

    logging.debug("Calling remove_comment_from_line()")

    if COMMENT_TOKEN not in line:
        return line

    if line[0] == COMMENT_TOKEN:
        for i in ADMITTED_COMMENTS:
            if line[i] == ADMITTED_COMMENTS[i]:
                return line

        return []

    # Fix COMMENT_TOKEN in strings
    # a string is defined with c"......."
    i = 0
    remove = True

    line_length = len(line)

    for i in range(0, line_length):

        if i+1 < line_length:
            if line[i] == 'c' and line[i+1] == '"':
                remove = False

        elif not remove and line[i] == '"':
            remove = True

        elif remove and line[i] == COMMENT_TOKEN:
            return line[:i]

    return line


def remove_unrelevant_spaces(line):
    """
    Removes all unrelevant spaces from the line.
    """

    logging.debug("Calling remove_unrelevant_spaces()")
    # spaces that are not between "" or '' aren't relevant
    tokens = ['"', '\'']

    # if no ' or " exists in the line, no relevant spaces exists either
    if tokens[0] not in line and tokens[1] not in line:
        return tools.list_sanitize(line, TOKEN_SPACE)

    i = 0
    stop_token = None

    while i < len(line):
        token = line[i]

        # do not remove spaces
        if token in tokens:
            # stop removing spaces
            if stop_token is None:
                stop_token = token
            # restart removing spaces, only if stop_token found
            elif stop_token == token:
                stop_token = None
        
        # if stop_token is not set, remove spaces and do not increment i
        # since all the list will be left-shifted
        if stop_token is None and token == TOKEN_SPACE:
            del line[i]
        else:
            i += 1

    return line


def collapse_switch_statement(text):
    """
    Properly treats the switch statement.
    Is is over multiple lines, so it collapses them into a single one.
    To recognise the paramenters on the new line, SWITCH_NEW_LINE_MARKER is used.
    """

    logging.debug("Calling collapse_switch_statement()")

    collapsed_text = []

    i = 0

    while i < len(text):
        element = text[i]

        if element[0] == 'switch':
            # find the index of the next list containing the closing ] of the switch
            for j in range(i+1, len(text)):
                if text[j][0] == ']':
                    break
                else:
                    # append new line marker
                    text[j].append(SWITCH_NEW_LINE_MARKER)

            # get a flat list from a list of lists
            element = tools.flat_list(text[i:j+1])

            # index update
            i = j
        
        collapsed_text.append(element)

        i = i + 1

    return collapsed_text
