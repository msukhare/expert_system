OPERATOR = ('(', ')', '!', '+', '|', '^', '=>', '<=>')

def check_if_operator(line):
    for opera in OPERATOR:
        if line.startswith(opera):
            return opera
    return ""

def lexing_line(line):
    i = 0
    tokens = []
    while (i < len(line)):
        operator = check_if_operator(line[i:])
        if operator:
            i += len(operator)
            tokens.append(operator)
        elif line[i] == '#':
            return tokens
        else:
            if line[i].isspace() == False:
                tokens.append(line[i])
            i += 1
    return tokens
