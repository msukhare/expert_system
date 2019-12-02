import sys
import os.path
from read_file_with_info import read_file
from inference_engine import inf_engine
from shell import interactive_shell

def print_tree(rule, pos, deepth):
    print(rule.value, pos, deepth)
    if rule.left is not None:
        print_tree(rule.left, "left", deepth + 1)
    if rule.right is not None:
        print_tree(rule.right, 'right', deepth + 1)

def main():
    inference_engine = read_file()
    inference_engine.execute()
    interactive_shell(inference_engine)

if __name__ == "__main__":
    ### check number argument, one argument must be present
    if len(sys.argv) != 2:
        sys.exit("Missing file to analyse.\nUsage: pythonX.X example_input.txt")
    ### check if file exists
    if os.path.exists(sys.argv[1]) == False:
        sys.exit("%s doesn't exists" %sys.argv[1])
    ### check if argv is a file
    if os.path.isfile(sys.argv[1]) == False:
        sys.exit("%s isn't a file" %sys.argv[1])
    main()

