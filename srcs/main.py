import sys
import os.path
from read_file_with_info import read_file

def main():
    rules, facts, queries = read_file()

if __name__ == "__main__":
    ### check number argument, one argument must be present
    if len(sys.argv) <= 1 or len(sys.argv) > 2:
        sys.exit("Missing file to analyse.\nUsage: pythonX.X example_input.txt")
    ### check if file exists
    if os.path.exists(sys.argv[1]) == False:
        sys.exit("%s doesn't exists" %sys.argv[1])
    ### check if argv is a file
    if os.path.isfile(sys.argv[1]) == False:
        sys.exit("%s isn't a file" %sys.argv[1])
    main()
