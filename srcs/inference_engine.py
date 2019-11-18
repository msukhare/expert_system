def not_op(left, right):
    if left is False:
        return True
    return False

def and_op(left, right):
    if left is True and right is True:
        return True
    return False

def or_op(left, right):
    if left is True or right is True:
        return True
    return False

def xor_op(left, right):
    if left is True and right is False or left is False and right is True:
        return True
    return False

dictionnary_of_rules = {'!': not_op, '+': and_op, '|': or_op, '^': xor_op, '=>': None, '<=>': None}

class inf_engine():
    def __init__(self):
        self.rules = {}
        self.facts = None
        self.queries = None

    def execute_tree(self, rule):
        if rule is None:
            return None
        left = self.execute_tree(rule.left)
        right = self.execute_tree(rule.right)
        if rule.operator is True:
            return dictionnary_of_rules[rule.value](left, right)
        return self.compute_state_querie(rule.value)

    def compute_conclusion(self, tree):
        if tree.value == '!':
            return False
        return True

    def get_status_querie(self, querie):
        if querie in self.facts:
            state_before = True
        else:
            state_before = None
        for i in range(len(self.rules[querie])):
            if self.rules[querie][i].status is True:
                state = self.compute_conclusion(self.rules[querie][i].right)
                if state is True and state_before is False:
                    return None
                elif state is False and state_before is True:
                    return None
                state_before = state
        return state_before

    def compute_state_querie(self, querie):
        if querie in self.facts and querie not in self.rules:
            return True
        if querie not in self.rules:
            return False
        for rule in self.rules[querie]:
            if rule.checked is False:
                rule.checked = True
                rule.status = self.execute_tree(rule.left)
        return self.get_status_querie(querie)

    def execute(self):
        for querie in self.queries[1:]:
            state_querie = self.compute_state_querie(querie)
            if state_querie is True:
                print("%c is True" %querie)
            elif state_querie is False:
                print("%c is False" %querie)
            else:
                print("%c is False, two different rule" %querie)
