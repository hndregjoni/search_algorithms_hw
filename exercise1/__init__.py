from typing import List
from .solution import *
from common.solvers import BFSolver

goal = FlipState([[True]*3]*3, label = 'G')

def exercise1(argv: List[str]):
    initial = read_from_file("exercise1/input.txt")

    solver = BFSolver(initial, goal)

    result = solver.solve()

    print_backwards(result)
