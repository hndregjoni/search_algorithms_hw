from typing import List
from urllib.request import ProxyBasicAuthHandler
from .solution import *
from common.solvers import BFSolver, Solver, UniformCostSolver
from common.frontiers import PriorityQueeFrontier, QueueFrontier, StackFrontier

goal = FlipState([[True]*3]*3, label = 'G')

def exercise1(argv: List[str]):
    initial = read_from_file("exercise1/input.txt")

    g = lambda s: s.last.cost + 1 if s.last is not None else s.cost
    # solver = UniformCostSolver(initial, goal, g)
    solver = Solver(initial, goal, QueueFrontier())

    result = solver.solve()

    print_backwards(result)
