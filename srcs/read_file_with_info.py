import sys
import copy
from lexer import lexing_line
from parser import if_parser
from inference_engine import inf_engine

def check_if_operator(line):
    for opera in OPERATOR:
        if line.startswith(opera):
            return opera
    return ""

def swap_assignation(parsed):
    parsed[0].value = '=>'
    sec_rule = copy.deepcopy(parsed[0])
    tmp = sec_rule.left
    sec_rule.left = sec_rule.right
    sec_rule.right = tmp
    parsed.append(sec_rule)
    return parsed

def create_new_rule(from_rule, store, rule):
    tmp = copy.deepcopy(from_rule)
    tmp.right = rule
    if rule.value == '!':
        store.append((rule.left.value, tmp))
    else:
        store.append((rule.value, tmp))

def extract_operands(rule, store, principale_rule):
    if rule.operator is True and rule.value == '|' or rule.value == '^':
        raise SyntaxError("| and ^ can't be in conclusion of rule")
    if rule.operator is True and rule.value == '!' and rule.left.operator is True:
        raise SyntaxError("In conclusion, after ! must be an operand")
    if rule.left is not None and rule.value != '!':
        extract_operands(rule.left, store, principale_rule)
    if rule.right is not None and rule.value != '!':
        extract_operands(rule.right, store, principale_rule)
    if rule.operator is True and rule.value == '!':
        create_new_rule(principale_rule, store, rule)
    elif rule.operator is False:
        create_new_rule(principale_rule, store, rule)

def print_tree(rule, pos, deepth):
    print(rule.value, pos, deepth)
    if rule.left is not None:
        print_tree(rule.left, "left", deepth + 1)
    if rule.right is not None:
        print_tree(rule.right, 'right', deepth + 1)

def format_rules(parsed, rules):
    if parsed[0].value == '<=>':
        parsed = swap_assignation(parsed)
    for ele in parsed:
        tmp = []
        extract_operands(ele.right, tmp, ele)
        for new_key in tmp:
            if new_key[0] in rules:
                rules[new_key[0]].append(new_key[1])
            else:
                rules[new_key[0]] = [new_key[1]]

def read_file():
    """
    Read line by line file in sys.argv and delete space backslash n and backslash t. Split with
    # and extract first ele
    params: None
    return: engine --> class inf_engine conatain rules, facts, queries
    """
    engine = inf_engine()
    with open(sys.argv[1], 'r') as fd:
        for line in fd:
            tmp = lexing_line(line)
            if tmp:
                if tmp[0] == '=' and engine.rules and engine.queries is None:
                    engine.facts = tmp
                elif tmp[0] == '?' and engine.rules and engine.facts is not None:
                    engine.queries = tmp
                elif tmp[0] != '=' and tmp[0] != '?' and engine.queries is None and\
                        engine.facts is None:
                    try:
                        format_rules([if_parser(tmp)], engine.rules)
                    except SyntaxError as to_print:
                        sys.stderr.write("SyntaxError: %s in %s" %(str(to_print), line))
                    except RecursionError:
                        sys.stderr.write("Error: %s must be less complexe" %line)
                else:
                    raise Exception("Wrong formatage of file %s" %sys.argv[1])
    return engine
