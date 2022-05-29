from typing import List
from urllib.request import ProxyBasicAuthHandler
from .solution import *
from common.solvers import BFSolver, Solver, UniformCostSolver
from common.frontiers import PriorityQueeFrontier, QueueFrontier, StackFrontier, uniform_distance
from common.state import print_forward_solution

goal = FlipState([[1]*3]*3, label = 'G')

def exercise1(argv: List[str]):
    initial = read_from_file("exercise1/input.txt")

    # solver = UniformCostSolver(initial, goal, uniform_distance)
    solver = Solver(initial, goal, QueueFrontier())

    result = solver.solve()

    print_forward_solution(result)
