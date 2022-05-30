from typing import List, Any

from argparse import ArgumentParser
from io import TextIOWrapper
from sys import stdin, stdout

from common.gui import SolutionDisplay

from exercise1 import exercise1
from exercise2 import exercise2
from exercise3 import exercise3
from exercise4 import exercise4

EXERCISES = {
    "1": (exercise1, True),
    "2": (exercise2, True),
    "3": (exercise3, False),
    "4": (exercise4, True)
}

def write_steps_to(out: TextIOWrapper, steps: List[str]):
    out.write(str(len(steps)) + "\n")
    out.writelines(steps)

def err(mess: str):
    print(mess)
    exit()

def map_to_str(s: Any):
    return repr(s) + "\n"

# Args
parser = ArgumentParser(description="Run the exercises")

parser.add_argument("--exercise", type=str, help="The exercise number to run")
parser.add_argument("--gui", action="store_true", help="Enable GUI?")

parser.add_argument('--stdin', action="store_true", help="Use stdin for input")
parser.add_argument('--input', type=str, required=False, help="Use the given file for input")

parser.add_argument('--stdout', action="store_true", help="User stdout for output")
parser.add_argument('--output', type=str, required=False, help="User the given file for output")

parser.add_argument("--algorithm", type=str, help="Specify the algorithm (lfs, dfs, astar (with specified heuristic), uniform")

if __name__ == "__main__":
    out_f: TextIOWrapper

    args = parser.parse_args()

    ex_args = {
        "gui": args.gui,
        "algorithm": args.algorithm
    }

    if args.exercise not in EXERCISES:
        err("Exercise specified does not exist")

    if args.input is not None:
        ex_args["path"] = args.input
    elif args.stdin == True:
        ex_args["file"] = stdin
    else:
        err("Specify some input method!")
     
    # one_to_one is used to store whether there is one image per one state
    to_run, one_to_one = EXERCISES[args.exercise]

    if args.output is not None:
        out_f = open(args.output)
    elif args.stdout == True:
        out_f = stdout
    else:
        err("Specify some output method!")


    if args.gui == True:
        steps, images = to_run(**ex_args)

        # Map to string:
        steps = [*map(map_to_str, steps)]

        if len(steps) == 0:
            err("No solution")
        
        write_steps_to(out_f, steps)

        # tkinter
        display = SolutionDisplay(steps if one_to_one else None, images)
        display.mainloop()
    else:
        steps = to_run(**ex_args)

        # Map to string:
        steps = [*map(map_to_str, steps)]

        write_steps_to(out_f, steps)
    
    if not args.stdout == True:
        out_f.close()