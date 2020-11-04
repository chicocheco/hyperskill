def re_equal_len(regex, string):
    """When regex is of the same length as input string"""
    if not regex:  # regex consumed
        return True
    if not string:
        if regex == "$":
            return True
    elif regex[0] == '\\':
        if not regex[1] == string[0]:
            return False
        return re_equal_len(regex[2:], string[1:])
    else:
        if len(regex) >= 2:
            if regex[1] == '?':
                return re_equal_len(regex[2:], string) or \
                       re_equal_len(regex[0] + regex[2:], string)
            if regex[1] == '*':  # 1st case == 1st case of '?'
                return re_equal_len(regex[2:], string) or \
                       re_equal_len(regex, string[1:])
            if regex[1] == '+':  # 1st case == 2nd case of '?' and 2nd case == 2nd of '*'
                return re_equal_len(regex[0] + regex[2:], string) or \
                       re_equal_len(regex, string[1:])
        if regex[0] == string[0] or regex[0] == '.':
            return re_equal_len(regex[1:], string[1:])
    return False  # string consumed


def re_unequal_len(regex, string):
    i = 0
    while True:
        shift_string = string[i:]
        is_match = re_equal_len(regex, shift_string)
        if is_match or not shift_string:
            break
        i += 1
    return is_match


def regex_func(regex, string):
    if regex.startswith('^'):
        return re_equal_len(regex.strip('^'), string)
    return re_unequal_len(regex.strip('^'), string)


if __name__ == '__main__':
    in_regex, in_string = input().split('|')
    print(regex_func(in_regex, in_string))
