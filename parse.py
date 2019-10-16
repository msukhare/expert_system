import string

class ast():
    def __init__(self):
        self.type = 'operateur' or 'operande'
        self.value = 10
        self.left = 0
        self.right = 0
        #self.

def check_line(line):
    accepted = ['+', '|', '^', '(', ')', '=', '<', '>', '!']
    for i in range(0, len(line)-2):
        if line[i] not in accepted and line[i] not in string.ascii_uppercase:
            print("ERREUR1", line[i])
            return False
    for i in range(0, len(line)-1):
        #if line[i] == '<' and line[i+1] == '=':
        #    continue
        if line[i] == '=' and line[i+1] == '>':
            continue
        if line[i] in string.ascii_uppercase and line[i+1] not in accepted:
            print("ERREUR2")
            return False
    return True

def clear_text(line):
    if line == "" or line[0] == '#':
        return None
    for i in range(0, len(line)):
        if line[i] == '#':
            line = line[:i]
            break
    is_fine = check_line(line)
    if is_fine == False:
        return None
    return line

def print_calcul(expression):
    #print(expression)
    for i in range(0, len(expression)):
        #print(type(expression[i]))
        #print(expression[i])
        if type(expression[i]['left']) == dict or type(expression[i]['left']) == list:
            print('(')
            print_calcul(list(expression[i]['left']))
            print(')')
        else:
            print(expression[i]['left'])
            print(expression[i]['value'])
        if type(expression[i]['right']) == dict or type(expression[i]['right']) == list:
            print('(')
            print_calcul(list(expression[i]['right']))
            print(')')
        else:
            print(expression[i]['right'])
        #print(expression[i])

def priority(expression):
    priority = {'^': 1, '|':2, '+':3}
    parenthese = 0
    for i in range(0, len(expression)):
        if expression[i] == '(':
            parenthese += 3
        elif expression[i] == ')':
            parenthese -= 3
        elif expression[i] in ['^', '|', '+']:
            expression[i] = {"value": expression[i],
                            "priority": priority[expression[i]] + parenthese}
    return expression


def create_tree(tree, expression, index):
    print("Create")
    print(expression)
    smallest_priority = {'index': None, 'value': None}
    count = 0
    for i in range(0, len(expression)):
        if type(expression[i]) == dict:
            count += 1
            if (smallest_priority['value'] == None
            or expression[i]['priority'] < smallest_priority['value']):
                smallest_priority['index'] = i
                smallest_priority['value'] = expression[i]['priority']
    if smallest_priority['index'] == None:
        if len(expression) > 1:
            return '!' + expression[1]
        return expression
    if count <= 1:
        i = smallest_priority['index']
        if expression[i+1] == '!':
            right = '!' + expression[i+2]
        else:
            right = expression[i+1]
        if i > 1 and expression[i-2] == '!':
            left = '!' + expression[i-1]
        else:
            left = expression[i-1]
        tree = {"value": expression[i]['value'],
                    "left": left,
                    'right': right}
        return tree
    i = smallest_priority['index']
    tree = {"value": expression[i]['value'],
                   "left": create_tree(tree, expression[0:i], index+1),
                    'right': create_tree(tree, expression[i+1:], index+1)}
    return tree


def test(line):
    if "<=>" in line:
        eq = "<=>"
    else:
        eq = "=>"
    expression, conclusion = line.split("=")
    expression = list(expression)
    print(expression)
    expression = priority(expression)
    i = 0
    length = len(expression)
    while i < length:
        if type(expression[i]) == str and expression[i] in ['(', ')']:
            del expression[i]
            i -= 1
            length -= 1
        i += 1
    tree = {}
    tree = create_tree(tree, expression, 0)
    print(tree, "\n\n\n")
    # while i < length:
    #     if type(expression[i]) == str:
    #         del expression[i]
    #         i -= 1
    #         length -= 1
    #     i += 1
    #print_calcul(expression)
    #print(expression, "\n\n")


def add_element(tree, line):
    line = line.strip()
    line = line.replace(" ", "")
    line = clear_text(line)
    if line == None:
        return
    #add element
    test(line)
    #create_tree(line)
    return tree

def set_knowledge(knowledge, line):
    return knowledge

def set_goal(goals, line):
    return goals

def read_input():
    tree = ast()
    knowledge = {}
    goals = {}
    print("Vous devez entrer les règles et la valeur de départ puis finir avec les valeurs recherché(la ligne doit commencé par '?')")
    while True:
        line = input()
        if line == "":
            continue
        if line[0] not in ['=', '?']:
            tree = add_element(tree, line)
        elif line[0] == '=':
            knowledge = set_knowledge(knowledge, line)
        elif line[0] == '?':
            goals = set_goal(goals, line)
            break
    return tree

def create_ast():
    tree = read_input()
    return tree