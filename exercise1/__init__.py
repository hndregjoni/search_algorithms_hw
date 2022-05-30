from turtle import forward
from typing import List, Tuple, cast
from urllib.request import ProxyBasicAuthHandler

from common.graphics import draw_grid_state
from .solution import *
from common.solvers import BFSolver, Solver, UniformCostSolver
from common.frontiers import PriorityQueeFrontier, QueueFrontier, StackFrontier, uniform_distance
from common.state import forward_solution, print_forward_solution

from PIL.Image import Image

goal = FlipState([[1]*3]*3, label = 'G')

def run_with_snapshots(solver: Solver[FlipState]):
    images: List[Image] = []

    result = solver.solve()

    steps = forward_solution(result)
    for step in steps:
        images.append(draw_grid_state(cast(FlipState, step)))
    
    return steps, images

def exercise1(path: str, file: TextIOWrapper = None, gui: bool = False):
    if path:
        initial = read_from_file(path)
    else:
        initial = read_from_open_file(file)

    # solver = UniformCostSolver(initial, goal, uniform_distance)
    solver = Solver(initial, goal, QueueFrontier())

    if gui:
        return run_with_snapshots(solver)
    else:
        result = solver.solve()
        return forward_solution(result)