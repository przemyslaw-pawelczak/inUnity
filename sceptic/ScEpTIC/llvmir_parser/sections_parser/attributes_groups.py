import logging

from ScEpTIC.exceptions import ParsingException
from ScEpTIC import tools


def parse_attributes_groups_section(text, log_section_content = False):
    """
    Parse and return the attributes groups section, using parse_attributes_group.
    attributes #0 = { alwaysinline alignstack=4 ...}
    """

    logging.debug('Calling parse_attributes_groups_section({}, {})'.format(text, log_section_content))
    
    attributes_groups = {}

    for line in text:
        attributes_group = parse_attributes_group(line)
        attributes_groups[attributes_group['name']] = attributes_group

    if logging.getLogger().isEnabledFor(logging.INFO):
        log_str = 'Parsed attributes groups section. {} attributes groups found'.format(len(attributes_groups))

        if log_section_content:
            log_str += ':\n{}'.format(tools.fancy_dict_to_str(attributes_groups))
        else:
            log_str += '.\n{}'.format(tools.fancy_dict_keys_to_str(attributes_groups))

        logging.info(log_str)

    return attributes_groups


def parse_attributes_group(text):
    """
    Parses a line containing a list of attributes and returns the id of the attributes group and the attributes themselves.
    Valued attributes will be represented as a list ['attribute_name', 'attribute_value']
    """

    logging.debug('Calling parse_attributes({})'.format(text))

    # an attributes definition must be with attributes #int = { ... }
    if not is_attributes_group(text):
        raise ParsingException('LLVM IR Syntax error. attributes #id = {...} expected.'+' {}...{} given'.format(tools.list_join(text[0:5], ' '), text[-1]))
    
    # name is on position 2
    name = '#'+text[2]

    # remove attribute #name = { ... } and keep only inside part
    text = text[5:-1]
    attributes = []
    
    i = 0

    while i < len(text):
        val = text[i]
        
        # if is a string
        if val == '"':
            # get position of closing "
            closing = text.index('"', i+1)

            # retrieve value inside " ... "
            val = tools.list_join(text[i+1:closing])
            
            # update index to be parsed
            i = closing + 1

            # if is a key=value
            if text[i] == '=':
                i += 1
                # "key" = "value"
                if text[i] == '"':
                    closing = text.index('"', i+1)
                    val = {val: tools.list_join(text[i+1:closing])}
                    i = closing + 1
                else:
                    val = {val: text[i]}
                    i += 1
        else:
            i += 1

        attributes.append(val)

    attributes = {'name': name, 'attributes': attributes}

    if logging.getLogger().isEnabledFor(logging.DEBUG):
        log_vals = " {}".format(attributes)
        logging.debug('Parsed attribute {}:\n{}'.format(name, tools.instert_new_line_every(log_vals, new_line_padding = ' ')))

    return attributes


def is_attributes_group(text):
    """
    Return if the line represents an attributes group.
    """

    logging.debug('Calling is_attributes_group({})'.format(text))

    return isinstance(text, list) and len(text) > 5 and text[0] == 'attributes' and text[1] == '#' and text[3] == '=' and text[4] == '{' and text[-1] == '}'
