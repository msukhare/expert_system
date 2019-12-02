import sys

CYCLE = 2

def not_op(left, right):
    if left == CYCLE:
        return CYCLE
    if left is None or left is False:
        return True
    return None

def and_op(left, right):
    if left == CYCLE or right == CYCLE:
        return CYCLE
    if left is True and right is True:
        return True
    return None

def or_op(left, right):
    if left == CYCLE and right == CYCLE:
        return CYCLE
    if left is True or right is True:
        return True
    return None

def xor_op(left, right):
    if left == CYCLE or right == CYCLE:
        return CYCLE
    if left is True and (right is None or right is False) or (left is None or left is False) and\
        right is True:
        return True
    return None

dictionnary_of_rules = {'!': not_op, '+': and_op, '|': or_op, '^': xor_op, '=>': None, '<=>': None}

class InferenceError(Exception):
    def __init__(self, message):
        super().__init__(message)

class inf_engine():
    def __init__(self):
        self.rules = {}
        self.facts = None
        self.queries = None

    def execute_tree(self, tree):
        if tree is None:
            return None
        left = self.execute_tree(tree.left)
        right = self.execute_tree(tree.right)
        if tree.operator is True:
            return dictionnary_of_rules[tree.value](left, right)
        return self.compute_state_querie(tree.value)

    def compute_conclusion(self, tree):
        if tree.value == '!':
            tmp = self.compute_conclusion(tree.left)
            if tmp is True:
                return False
            return True
        return True

    def check_other_status(self, querie):
        if querie in self.facts:
            return False
        for rule in self.rules[querie]:
            if rule.status != CYCLE:
                return False
        return True

    def get_final_status_querie(self, querie):
        cycle = False
        if querie in self.facts:
            state_before = True
        else:
            state_before = None
        for ele in self.rules[querie]:
            if ele.status is True and state_before is False or\
                ele.status is False and state_before is True:
                raise InferenceError("(%c can't be True and False at the same time)" %querie)
            if ele.status is not None and ele.status != CYCLE:
                state_before = ele.status
            elif ele.status == CYCLE and self.check_other_status(querie) is True:
                cycle = True
        if cycle is True:
            return CYCLE
        return state_before

    def compute_state_querie(self, querie):
        if querie not in self.rules and querie in self.facts:
            return True
        if querie not in self.rules:
            return None
        for rule in self.rules[querie]:
            if rule.checked is False:
                rule.checked = True
                tmp = self.execute_tree(rule.left)
                if tmp is True:
                    rule.status = self.compute_conclusion(rule.right) 
                elif tmp == CYCLE:
                    rule.status = CYCLE
                rule.checked = False #to delete
            else:
                rule.status = CYCLE
        return self.get_final_status_querie(querie)

    def clear_rules(self):
        for key in self.rules.keys():
            for rule in self.rules[key]:
                rule.status = None
                rule.checked = False

    def execute(self):
        if self.facts is None:
            self.facts = ['=']
        if self.queries is None:
            self.queries = ['?']
        for querie in self.queries[1:]:
            try:
                state_querie = self.compute_state_querie(querie)
                if state_querie is True:
                    print("%c is True" %querie)
                elif state_querie == CYCLE:
                    print("%c is False, (Cycle detected.)" %querie)
                else:
                    print("%c is False" %querie)
            except InferenceError as error_to_print:
                print("%c is False, %s" %(querie, str(error_to_print)))
        self.clear_rules()
        sys.stdout.write('\n')

