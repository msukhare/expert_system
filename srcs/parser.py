
class ast():
    def __init__(self, value, operator, left, right):
        self.value = value
        self.operator = operator
        self.status = None
        self.checked = False
        self.left = left
        self.right = right

def atom_parser(stream):
    if not stream:
        raise SyntaxError("Unexcepted EOF")
    if stream[0].isupper() == True:
        return ast(stream[0], False, None, None), 1
    if stream[0] == '(':
        right, current_r = xor_parser(stream[1:])
        if current_r < len(stream) and stream[current_r + 1] == ')':
            return right, current_r + 2
        raise SyntaxError("Missing )")
    raise SyntaxError("Only upper case are accepted as operand")

def not_parser(stream):
    if stream[0] == '!':
        left, current = not_parser(stream[1:])
        return ast(stream[0], True, left, None), current + 1
    return atom_parser(stream)

def and_parser(stream):
    left, current = not_parser(stream)
    if current < len(stream) and stream[current] == '+':
        right, current_r = and_parser(stream[current + 1:])
        return ast(stream[current], True, left, right), current + current_r + 1
    return left, current

def or_parser(stream):
    left, current = and_parser(stream)
    if current < len(stream) and stream[current] == '|':
        right, current_r = or_parser(stream[current + 1:])
        return ast(stream[current], True, left, right), current + current_r + 1
    return left, current

def xor_parser(stream):
    left, current = or_parser(stream)
    if current < len(stream) and stream[current] == '^':
        right, current_r = xor_parser(stream[current + 1:])
        return ast(stream[current], True, left, right), current + current_r + 1
    return left, current

def if_parser(stream):
    left_part, current = xor_parser(stream)
    if current >= len(stream):
        raise SyntaxError("Missing assignation and expression")
    if stream[current] != '=>' and stream[current] != '<=>':
        raise SyntaxError("Missing assignation")
    if not stream[current + 1:]:
        raise SyntaxError("Missing expression after assignation")
    right_part, current_r = xor_parser(stream[current + 1:])
    return ast(stream[current], True, left_part, right_part)
