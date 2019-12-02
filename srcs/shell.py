import sys
from lexer import lexing_line

def interactive_shell(inference_engine):
    for line in sys.stdin:
        if line[0] == '=':
            inference_engine.facts = lexing_line(line)
        elif line[0] == '?':
            inference_engine.queries = lexing_line(line)
            inference_engine.execute()
