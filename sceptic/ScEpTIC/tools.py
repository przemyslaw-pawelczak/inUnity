import copy
import itertools
import re

def split_into_sublist(lst, separator):
    """
    Splits the list into sublists.
    separator will be used as split element and won't be present in the sublists.
    """

    return [list(group) for k, group in itertools.groupby(lst, lambda x: x == separator) if not k]


def split_context_into_sublist(lst, separator, start_tokens = ['(', '[', '{', '<'], end_tokens = [')', ']', '}', '>']):
    """
    Split the list into sublists.
    Elements between start_token and end_token are not splitted.
    e.g. split_context_into_sublist(, ',', ['{'], ['}'])
    ['line', ':', '18', ',', 'test', ':', '!', '{', '!', '3', ',', '!', '5', ',', '!', '6', '}']
    returns
    [['line', ':', '18'], ['test', ':', '!', '{', '!', '3', ',', '!', '5', ',', '!', '6', '}']]
    """

    new_list = []
    sub_list = []
    
    opened_tokens = []

    for i in range(0, len(start_tokens)):
        opened_tokens.append(0)

    for i in range(0, len(lst)):
        element = lst[i]

        # increment / decrement opened tokens
        if element in start_tokens:
            index = start_tokens.index(element)
            opened_tokens[index] += 1
        elif element in end_tokens:
            index = end_tokens.index(element)
            opened_tokens[index] -= 1

        # if not separator or inside start_token ... end_token, do not split
        # otherwise close the sublist and create next ones.
        if sum(opened_tokens) > 0 or element != separator:
            sub_list.append(element)
        else:
            new_list.append(sub_list)
            sub_list = []

    if len(sub_list) > 0:
        new_list.append(sub_list)

    return new_list


def get_index_in_context(lst, index, start_tokens = ['(', '[', '{', '<'], end_tokens = [')', ']', '}', '>']):
    """
    Return the index of the element "index" inside list lst.
    Elements between start_token and end_token are not considered as valid indexes.
    (Usefule to split / find subgroups [a, b] , [c, d])
    """

    opened_tokens = []

    for i in range(0, len(start_tokens)):
        opened_tokens.append(0)

    for i in range(0, len(lst)):
        element = lst[i]

        # increment / decrement opened tokens
        if element in start_tokens:
            token_index = start_tokens.index(element)
            opened_tokens[token_index] += 1
        elif element in end_tokens:
            token_index = end_tokens.index(element)
            opened_tokens[token_index] -= 1

        if sum(opened_tokens) == 0 and element == index:
            return i

    return None


def get_index_of_closed_par(lst, start_token, end_token):
    """
    Returns the index of a closed parentheses pair, considering the context as before.
    """

    opened = 0

    for i in range(0, len(lst)):
        element = lst[i]

        if element == start_token:
            opened += 1
        elif element == end_token:
            opened -= 1
            
            # return found index
            if opened == 0:
                return i
    return None


def get_indexes_of_matching_tokens(lst, start_token, end_token):
    start = None

    lst_len = len(lst)
    start_len = len(start_token)
    end_len = len(end_token)

    i = 0
    while i < lst_len:
        if i + start_len < lst_len and start is None:
            matches = 0

            for j in range(0, start_len):
                if start_token[j] == lst[i+j]:
                    matches += 1
                else:
                    break

            if matches == start_len:
                start = i
                i += start_len
                continue

        if i + end_len < lst_len and start is not None:
            matches = 0

            for j in range(0, end_len):
                if end_token[j] == lst[i+j]:
                    matches += 1
                else:
                    break

            if matches == end_len:
                return start, i+1

        i += 1

    return None


def split_parantheses_groups(lst, lpar = '[', rpar = ']'):
    """
    Splits a list into different parentheses groups.
    """

    new_list = []
    sub_list = []

    opened_par = 0

    for i in range(0, len(lst)):
        element = lst[i]
        sub_list.append(element)

        if element == lpar:
            opened_par += 1
        elif element == rpar:
            opened_par -= 1

            # on closing parenthesis, if no others are opened, split.
            if opened_par == 0:
                new_list.append(sub_list)
                sub_list = []

    if len(sub_list) > 0:
        new_list.append(sub_list)
        
    return new_list


def split_parantheses_groups_with_context(lst, lpar = '[', rpar = ']', start_token = '(', end_token = ')'):
    """
    Splits a list into different parentheses groups, but only if it is not inside a pair start_token - end_token.
    """

    new_list = []
    sub_list = []

    opened_par = 0
    opened_tokens = 0

    for i in range(0, len(lst)):
        element = lst[i]
        sub_list.append(element)

        if element == start_token:
            opened_tokens += 1
        elif element == end_token:
            opened_tokens -= 1
        elif element == lpar:
            opened_par += 1
        elif element == rpar:
            opened_par -= 1

            # on closing parenthesis, if no others are opened, split.
            if opened_par == 0 and opened_tokens == 0:
                new_list.append(sub_list)
                sub_list = []

    if len(sub_list) > 0:
        new_list.append(sub_list)
        
    return new_list


def list_sanitize(lst, element):
    """
    Removes all the occurrences of element from the list
    """

    return list(filter(lambda x: x != element, lst))


def list_sanitize_from_list(lst, elements):
    """
    Removes all the occurrences of any element in elements from the list
    """

    return list(filter(lambda x: x not in elements, lst))


def list_rebuild(lst, separator):
    """
    Joins the list into a single string and splits it using separator.
    """

    new_lst = list_join(lst)
    new_lst = new_lst.split(separator)
    
    while '' in new_lst:
        new_lst.remove('')

    return new_lst


def list_concat_elements(lst, element):
    """
    Concatenates the adjacent cell with the one containing only element.
    e.g. list_concat_elements(['a','+','b','c'], '+') produces ['a+b', 'c']
    """

    while element in lst:
        # index of central element
        index = lst.index(element)
        concat = list_join(lst[index-1:index+2])
        # rebuild list
        lst = lst[:index-1]+[concat]+lst[index+2:]

    return lst


def list_remove_sequence(lst, elements):
    """
    Removes a sequence of elements from a list.
    e.g. list_remove_sequence(['a', 'b', 'c', 'd'], ['b','c']) produces ['a', 'd']
    """

    offset = -1

    while True:
        try:
            # index of element. offset used to not considered already parsed indexes
            index = lst.index(elements[0], offset+1)
        except ValueError:
            return lst

        offset = index

        # if not exceeding the list
        if index + len(elements) <= len(lst):
            
            # verifies if elements contained in lst as a sequence
            for i in range(1, len(elements)):
                if lst[index+i] == elements[i]:
                    continue

                break

            # No break executed
            else:
                # remove len(elements) times lst[index]
                # element at len[index+1] will be at len[index] when len[index] is deleted
                for i in range(0, len(elements)):
                    del lst[index]

    return lst


def list_replace_element(lst, source, target):
    """
    Replace all the occurrences of source in lst with target
    """

    while source in lst:
        index = lst.index(source)
        lst[index] = target

    return lst


def list_to_string(lst, replace_elements = {}):
    """
    Converts a list to a string, replacing all the replace_elements.
    replace_elements must be a dictionary {'source': 'target', ...}
    """

    if len(replace_elements) > 0:
        for i in replace_elements:
            lst = list_replace_element(lst, i, replace_elements[i])

    return list_join(lst)

def list_to_string_using_boundaries(lst, start_token, end_token = None, continue_on_exception = False, replace_elements = {}):
    """
    Returns the string representing the sublist between the boundaries start_token and end_token.
    """

    try:
        start, end = get_list_boundaries(lst, start_token, end_token)
    except ValueError as e:
        if not continue_on_exception:
            raise e

        start = 0
        end = None

    return list_to_string(lst[start:end], replace_elements)


def get_list_boundaries(lst, start_token, end_token = None, right_most_end_token = False):
    """
    Return the start and end index to get all the element in a list that
    are between start_token and end_token (start/end tokens excluded)
    """

    if end_token is None:
        end_token = start_token

    start = lst.index(start_token) + 1

    if right_most_end_token:
        end = list_rindex(lst, end_token)
    else:
        end = lst.index(end_token, start)

    return start, end


def get_list_apex_boundaries(lst):
    """
    Returns the start and end delimiters for getting all the elements between "" or ''
    """

    try:
        start, end = get_list_boundaries(lst, '"')
    except ValueError:
        start, end = get_list_boundaries(lst, "'")

    return start, end


def list_rindex(lst, element):
    """
    Returns the right index of element in list lst.
    """

    return len(lst) - lst[-1::-1].index(element) - 1


def list_join(lst, elem = ''):
    """
    Joins a list
    """

    return elem.join(lst)


def flat_list(lst):
    """
    Flatterns a list of lists into a list
    """

    return [item for sublist in lst for item in sublist]


def fancy_list_to_str(lst, line_padding = '', expand_dict = False, max_line_length = 140):
    """
    Converts a list to a string with the line number in front of each line
    and inserts a new line separator every max_line_length characters.
    """

    converted_string = ""

    max_id = len(lst)
    max_id_length = len(str(max_id))

    # leading 0s format string
    id_format = '{:0'+str(max_id_length)+'}:'

    # new line padding
    new_line_padding = line_padding+' '*(max_id_length+3)

    for i in range(0, max_id):
        # format line number
        line_num = id_format.format(i)
        # format new line
        element = lst[i]
        if expand_dict and isinstance(element, dict):
            element = "\n"+fancy_dict_to_str(element, len(new_line_padding))

        line_text = "{}{} {}".format(line_padding, line_num, element)
        
        # add new line separators
        if not expand_dict or not isinstance(lst[i], dict):
            converted_string += instert_new_line_every(line_text, max_line_length, new_line_padding)+"\n"
        else:
            converted_string += line_text + "\n"

    return converted_string

def fancy_dict_to_str(lst, line_padding = 0, expand = False, max_line_length = 140):
    """
    Converts a dict to a string in a fancy way.
    """

    converted_string = ""

    keys = lst.keys()
    max_key_length = 0

    for i in keys:
        key_len = len(str(i))
        if key_len > max_key_length:
            max_key_length = key_len

    # add for ': '
    max_key_length = max_key_length + line_padding + 3

    for key in lst:
        # format line key
        line_key = format(str(key)+": ", '>'+str(max_key_length))
        # format new line
        element = lst[key]
        if isinstance(element, dict):
            element = "\n"+fancy_dict_to_str(element, max_key_length, expand)
        elif isinstance(element, list) and expand:
            element = "\n"+fancy_list_to_str(element, " "*max_key_length, expand)
        
        line_text = line_key + format(element)
        
        if '\n' not in line_text:
            line_text = instert_new_line_every(line_text, max_line_length, " "*max_key_length)
        # add new line separators
        converted_string += line_text+"\n"

    return converted_string


def fancy_dict_keys_to_str(lst):
    """
    Returns a string composed by only the keys of a given dictionary
    """

    converted_string = ""

    keys = list(lst)

    # use natural sorting / human sorting
    keys.sort(key=natural_keys)

    for i in keys:
        converted_string += "{}\n".format(i)

    return converted_string


def instert_new_line_every(line, max_line_length = 140, new_line_padding = ''):
    """
    Inserts a new line every max_line_length characters.
    To every new line is appendend new_line_padding
    """

    if len(line) <= max_line_length:
        return line

    converted_line = line[0:max_line_length]
    # remove processed lines
    line = line[max_line_length:]

    # calculate new max line length
    # every new line has a padding that must be added from its actual length
    sep = max_line_length - len(new_line_padding)

    while len(line) > 0:
        converted_line += "\n"+new_line_padding+line[:sep]
        line = line[sep:]

    return converted_line


def natural_keys(text):
    """
    https://nedbatchelder.com/blog/200712/human_sorting.html
    human sorting algoritm
    """

    return [atoi(c) for c in re.split('(\d+)', text)]


def atoi(text):
    return int(text) if text.isdigit() else text


def inf_depth_lst_flat(lst, flat_values = None):
    """
    Converts a very depth list of lists to a flat one and appends each element to flat_values
    """
    for el in lst:

        if isinstance(el, list):
            inf_depth_lst_flat(el, flat_values)
        
        else:
            flat_values.append(el)


def build_input_lookup_data(input_name, checkpoint_id):
    """
    Creates input lookup data given the input name and the checkpoint id.
    """

    if input_name is None or checkpoint_id is None:
        return {}
        
    return {checkpoint_id: [input_name]}


def merge_input_lookup_data(lookup, other):
    """
    Merges two input lookup data into a single one.
    """

    # copy lookups to not modify external data
    lookup = copy.deepcopy(lookup)
    other = copy.deepcopy(other)

    # if lookup empty -> return other
    if lookup is None or len(lookup) == 0:
        return other

    # if other empty (lookup is not if this got here) -> return lookup
    if other is None or len(other) == 0:
        return lookup

    for key in other:
        if key in lookup:
            # merge the two lists
            lookup[key] = list(set(lookup[key] + other[key]))
        else:
            lookup[key] = other[key]

    return lookup
