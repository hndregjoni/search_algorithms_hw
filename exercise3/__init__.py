from common.solvers import BFSolver
from .solution import *

def exercise3(argv: List[str]) -> None:
    initial, maze, goal = read_from_file()

    solver = BFSolver(initial, goal)

    result = solver.solve()

    print_backwards(result)