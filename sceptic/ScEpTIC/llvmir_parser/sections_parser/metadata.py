import logging

from ScEpTIC import tools
from ScEpTIC.AST.elements.metadata import Metadata
from ScEpTIC.exceptions import ParsingException, LLVMSyntaxErrorException, NotImplementedException
from ScEpTIC.llvmir_parser.token_generator import TOKEN_SPACE


def parse_metadata_section(text, log_section_content = False):
    """
    Parses and returns the metadata section, using parse_metadata.
    !name = [distinct] !(...)
    """

    logging.debug('Calling parse_metadata_section({}, {})'.format(text, log_section_content))

    for line in text:
        parse_metadata(line)
        
    metadatas = Metadata.elements

    if logging.getLogger().isEnabledFor(logging.INFO):
        log_str = 'Parsed metadata section. {} metadata found'.format(len(metadatas))

        if log_section_content:
            log_str += ':\n{}'.format(tools.fancy_dict_to_str(metadatas))

        else:
            log_str += '.\n{}'.format(tools.fancy_dict_keys_to_str(metadatas))

        logging.info(log_str)

    return metadatas


def parse_metadata(text):
    """
    Parses and returns a line containing metadata information.
    """

    logging.debug('Calling parse_metadata({})'.format(text))

    if not is_metadata(text):
        raise ParsingException('Metadata must start with "!". {} given.'.format(text))

    name = text[0]+text[1]

    retval = parse_metadata_body(text, name)

    if logging.getLogger().isEnabledFor(logging.DEBUG):
        log_vals = " {}".format(retval)
        logging.debug('Parsed metadata {}:\n{}'.format(name, tools.instert_new_line_every(log_vals, new_line_padding = ' ')))

    return retval


def get_metadata_right_side(text):
    """
    Remove useless tokens from metadata.
    """

    logging.debug('Calling extract_metadata_start({})'.format(text))

    try:
        index = text.index('!')

    except ValueError:
        raise LLVMSyntaxErrorException('Metadata right side must contain "!". {} given.'.format(text))

    return text[index+1:]


def get_metadata_body(text):
    """
    Returns the metadata body (text after = ).
    """

    logging.debug('Calling get_metadata_body({})'.format(text))

    try:
        start = text.index('=')

    except ValueError:
        raise ParsingException('Unable to parse given metadata: {}'.format(text))

    if text[0] != '!':
        raise ParsingException('LLVM IR syntax erorr! Metadata body must start with "!". {} given.'.format(text[0]))
    
    return get_metadata_right_side(text[start+1:])


def parse_metadata_body(text, metadata_name):
    """
    Parses and returns the body of a metadata.
    It returns a Metadata object.
    """

    logging.debug('Calling parse_metadata_body({}, {})'.format(text, metadata_name))

    body = get_metadata_body(text)
    
    # verify metadata type and parse accordingly
    if body[0] == '{':
        # collection
        return parse_metadata_collection(body, metadata_name)

    elif body[1] == '(':
        # metadata function
        return parse_metadata_function(body, metadata_name)

    else:
        raise NotImplementedException(body)


def parse_metadata_collection(text, metadata_name, raise_exception = True):
    """
    Parses a metadata collection and returns it.
    !id = {!elem (, !elem)*}
    """

    logging.debug('Calling parse_metadata_collection({}, {}, {})'.format(text, metadata_name, raise_exception))

    # find delimiters for elements
    try:
        start, end = tools.get_list_boundaries(text, '{', '}')

    except ValueError:
        if raise_exception:
            raise ParsingException('Metadata collection expected. {} given.'.format(text))

        else:
            return False

    # remove ! and "
    content = text[start:end]
    
    # get actual elements of the metadata by splitting the list with ,
    content = tools.split_into_sublist(content, ',')
    
    includes = []
    values = []

    for element in content:
        # metadata starts with ! and a number. e.g. !1
        if element[0] == '!' and element[1].isdigit():
            element_str = tools.list_to_string(element)
            includes.append(element_str)

            # skip to next element
            continue

        try:
            val = tools.list_to_string_using_boundaries(element, '"', continue_on_exception=True, replace_elements={TOKEN_SPACE: ' '})
            values.append(val)

        except ValueError:
            values.append(element)

    data = Metadata(metadata_name, 'collection', 'collection', values, includes)

    return data


def parse_metadata_function(text, metadata_name):
    """
    Parses all type of metadata functions and returns the parsed metadata function.
    """
    
    logging.debug('Calling parse_metadata_function({}, {})'.format(text, metadata_name))
    
    # get list of arguments (name, value)
    content = get_metadata_body_arg_list(text)
    
    values = {}

    for element in content:
        # name: value
        name = element[0]
        val = element[2:]

        # check if includes other metadata
        if val[0] == '!':
            collection = parse_metadata_collection(val, None, False)

            if collection:
                val = collection

            else:
                val = tools.list_to_string(val, {TOKEN_SPACE: ' '})

        else:
            # fetch actual value
            val = tools.list_to_string_using_boundaries(val, '"', continue_on_exception=True, replace_elements={TOKEN_SPACE: ' '})

        values[name] = val

    # text[0] contains the name of the metadata function

    data = Metadata(metadata_name, 'function', text[0], values, [])

    return data


def get_metadata_body_arg_list(text, do_split = True):
    """
    Returns the argument list of a metadata "function".
    """

    logging.debug('Calling get_metadata_body_arg_list({}, {})'.format(text, do_split))

    # find delimiters for elements
    try:
        start, end = tools.get_list_boundaries(text, '(', ')', right_most_end_token=True)

    except ValueError:
        raise LLVMSyntaxErrorException('Unable to find delimiters for metadata argument list. {}'.format(text))

    content = text[start:end]

    # get a list of elements-values
    if do_split:
        content = tools.split_context_into_sublist(content, ',')
        
    return content


def is_metadata(text):
    """
    Returns if parsed line represents metadata.
    """

    logging.debug('Calling is_metadata({})'.format(text))

    return isinstance(text, list) and len(text) > 1 and text[0] == '!'


def get_element_metadata(text, elem_name, return_index = False):
    """
    Returns the metadata associated to other instructions a line of llvm code.
    """

    logging.debug('Calling get_element_metadata({}, {}, {})'.format(text, elem_name, return_index))

    closed_par = [']', ')']
    
    metadata_abs_index = 0

    # get only metadata outside arguments
    for par in closed_par:

        try:
            metadata_base_index = tools.list_rindex(text, par) + 1
            metadata_abs_index += metadata_base_index
            text = text[metadata_base_index:]

        except ValueError:
            pass

    # !name !N
    metadata = {}
    metadata_start_index = 0
    token = '!'
    offset = 0

    while token in text[offset:]:
        # get index of metadata name
        index = text.index(token, offset) + 1
        
        if metadata_start_index == 0:
            # , ! name ! value
            # I need the index of the comma, which is index of first ! -2
            metadata_start_index = index - 2

        if text[index+1] != token:
            raise LLVMSyntaxErrorException('Invalid metadata for {}.'.format(elem_name))

        name = text[index]
        value = text[index+1]+text[index+2]
        
        if name in metadata:
            metadata[name].append(value)
        else:
            metadata[name] = [value]

        offset = index + 3

    if len(metadata) == 0:
        logging.warning('No metadata information present for {}.'.format(elem_name))
        metadata_start_index = 0
        metadata_abs_index = 0

    # only debug metadata relevant for my application
    if 'dbg' in metadata:
        metadata = Metadata(None, 'collection', 'collection', [], metadata['dbg'])
        
    else:
        metadata = None
        
    if return_index:
        return metadata, (metadata_start_index + metadata_abs_index)

    return metadata
