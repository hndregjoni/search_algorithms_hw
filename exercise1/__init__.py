from typing import List, Tuple
from urllib.request import ProxyBasicAuthHandler

from common.graphics import draw_grid_state
from .solution import *
from common.solvers import BFSolver, Solver, UniformCostSolver
from common.frontiers import PriorityQueeFrontier, QueueFrontier, StackFrontier, uniform_distance
from common.state import forward_solution, print_forward_solution

from PIL.Image import Image

goal = FlipState([[1]*3]*3, label = 'G')

def run_with_snapshots(solver: Solver[FlipState]) -> Tuple[Optional[FlipState], List[Image]]:
    images: List[Image] = []

    result = solver.solve()

    steps = forward_solution(result)
    for step in steps:
        images.append(draw_grid_state(step))
    
    return result, images

def exercise1(argv: List[str]):
    initial = read_from_file("exercise1/input.txt")

    # solver = UniformCostSolver(initial, goal, uniform_distance)
    solver = Solver(initial, goal, QueueFrontier())

    # result = solver.solve()

    # print_forward_solution(result)

    return run_with_snapshots(solver)

