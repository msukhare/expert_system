import sys
from lexer import lexing_line

def check_if_only_alpha(tmp):
    for cara in tmp[1:]:
        if cara.isupper() == False:
            return False
    return True

def interactive_shell(inference_engine):
    for line in sys.stdin:
        tmp = lexing_line(line)
        if line[0] == '=':
            if check_if_only_alpha(tmp) is True:
                inference_engine.facts = tmp
            else:
                print("Unexcepted cara, only upper case are accepted")
        elif line[0] == '?':
            if check_if_only_alpha(tmp) is True:
                inference_engine.queries = tmp
                inference_engine.execute()
            else:
                print("Unexcepted cara, only upper case are accepted")
        else:
            print("nothing is done, missing = or ?")
