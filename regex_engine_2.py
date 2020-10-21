def regex_func(inp: str):
    regex, string = (list(i) for i in inp.split('|'))

    if not regex:  # regex consumed
        return True
    if string:
        if regex[0] == string[0] or regex[0] == '.':
            return regex_func(''.join(regex[1:]) + '|' + ''.join(string[1:]))
        else:
            return False
    else:
        return False


print(regex_func(input()))
