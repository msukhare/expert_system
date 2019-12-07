import sys
import copy
from lexer import lexing_line
from parser import if_parser
from inference_engine import inf_engine
from shell import check_if_only_alpha

def swap_assignation(parsed):
    """ This function is called if assignation is <=>, create two new AST
        params:
            parsed --> AST
        return:
            list --> [AST] or [AST, AST]
    """
    parsed[0].value = '=>'
    sec_rule = copy.deepcopy(parsed[0])
    tmp = sec_rule.left
    sec_rule.left = sec_rule.right
    sec_rule.right = tmp
    parsed.append(sec_rule)
    return parsed

def create_new_rule(from_rule, store, rule):
    """ Copy from rule to create new AST from rule, assigne equation to operand
        params:
            from_rule --> orignal rule, only left part stay
            store --> dict of rules
            rule --> from rule where extract operand
        return:
            None
    """
    tmp = copy.deepcopy(from_rule)
    tmp.right = rule
    if rule.value == '!':
        i = rule
        while (i.operator is True):
            i = i.left
        store.append((i.value, tmp))
    else:
        store.append((rule.value, tmp))

def check_if_other_operator_is_present(rule):
    """ Check if other operator is present in conclusion like | ^ or if get
        operator after !
        params:
            rule --> AST node
        return:
            Boolean --> True if operator is present, False if all ok
    """
    if rule is None:
        return False
    if rule.left is not None and rule.left.operator is True and rule.value == '!':
        return check_if_other_operator_is_present(rule.left)
    if rule.operator is True and rule.value != '!':
        return True
    return False

def extract_operands(rule, store, principale_rule):
    """ Extract operand at right of assignation and stock rule associate to operand 
        params:
            rule --> AST where extract operand
            store --> dict of rules
            principale_rule --> first node of AST
        return:
            None
    """
    if rule.operator is True and rule.value == '|' or rule.value == '^':
        raise SyntaxError("%c can't be in conclusion of rule" %rule.value)
    if rule.operator is True and rule.value == '!' and\
            check_if_other_operator_is_present(rule.left) is True:
        raise SyntaxError("In conclusion, after ! must be an operand")
    if rule.left is not None and rule.value != '!':
        extract_operands(rule.left, store, principale_rule)
    if rule.right is not None and rule.value != '!':
        extract_operands(rule.right, store, principale_rule)
    if rule.operator is False or rule.value == '!':
        create_new_rule(principale_rule, store, rule)

def format_rules(parsed, rules):
    """ Check if rule is <=>, if the double assignation create two new rule.
        Create one rule by operand in conclusion
        params:
            parsed --> list of rules
            rules --> dict where store new rules
        return:
            None
    """
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

class increase_recursion():
    """Increae number recursivity in stack"""
    def __init__(self, new_limit):
        """ Constructor of class
            params:
                new_limit --> new number of maximum recursion
        """
        self.new_limit = new_limit
        self.old_limit = sys.getrecursionlimit()

    def __enter__(self):
        """ set new limit when using class """
        sys.setrecursionlimit(self.new_limit)

    def __exit__(self, type, value, tb):
        """ set old limit when leave class """
        sys.setrecursionlimit(self.old_limit)

def read_file():
    """
    Read line by line file in sys.argv, delete space, backslash n and backslash t. Extract rules,
    facts and queries and return inf_engine class which contains rules, facts and queries.
    params:

    return:
        engine --> class inf_engine contain rules, facts, queries
    """
    engine = inf_engine()
    with open(sys.argv[1], 'r') as fd:
        for line in fd:
            tmp = lexing_line(line)
            if tmp:
                if tmp[0] == '=' and engine.queries is None:
                    if check_if_only_alpha(tmp) is True:
                        engine.facts = tmp
                    else:
                        print("Unexcepted cara, only upper case are accepted in %s" %line)
                elif tmp[0] == '?' and engine.facts is not None:
                    if check_if_only_alpha(tmp) is True:
                        engine.queries = tmp
                    else:
                        print("Unexcepted cara, only upper case are accepted in %s" %line)
                elif tmp[0] != '=' and tmp[0] != '?' and engine.queries is None and\
                        engine.facts is None:
                    try:
                        with increase_recursion(8000):
                            format_rules([if_parser(tmp)], engine.rules)
                    except SyntaxError as to_print:
                        sys.stderr.write("SyntaxError: %s in %s" %(str(to_print), line))
                    except RecursionError:
                        sys.stderr.write("Error: %s must be less complexe" %line)
    return engine
