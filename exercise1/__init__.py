from typing import List
from .solution import *
from common.solvers import BFSolver, Solver
from common.frontiers import QueueFrontier, StackFrontier

goal = FlipState([[True]*3]*3, label = 'G')

def exercise1(argv: List[str]):
    initial = read_from_file("exercise1/input.txt")

    # solver = BFSolver(initial, goal)
    solver = Solver(initial, goal, StackFrontier())

    result = solver.solve()

    print_backwards(result)
