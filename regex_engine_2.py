def regex_func(inp: str):
    regex, string = inp.split('|')

    if not regex:  # regex consumed
        return True
    if string:
        if regex[0] == string[0] or regex[0] == '.':
            return regex_func('|'.join((regex[1:], string[1:])))
        return False
    return False  # string consumed


print(regex_func(input()))
