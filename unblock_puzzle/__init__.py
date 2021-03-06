# Exercise 4

from typing import List, TextIO, Tuple, Optional, cast

from PIL.Image import Image

from common.solvers import AStarSolver, BFSolver, DFSolver, NoAlgorithmException, Solver, UniformCostSolver
from common.state import forward_solution, print_forward_solution
from common.frontiers import uniform_distance
from .solution import *
from .graphics import draw_unblock_state

def run_with_snapshots(solver: Solver[UnblockState]):
    images: List[Image] = []

    result = solver.solve()

    steps = forward_solution(result)
    for step in steps:
        images.append(draw_unblock_state(cast(UnblockState, step)))
    
    return steps, images

def goal(state: UnblockState) -> bool:
    """ This target assumes that the 0th tile is the main one 
    and also that it's always horizontal"""
    
    return state._state[0].coord[1] >= state.w

def exercise4(path: str, algorithm: str, file: TextIOWrapper = None, gui: bool = False):
    if path:
        initial = read_from_file(path)
    else:
        initial = read_from_open_file(file)

    heuristic = free_space_heuristic

    algorithm = algorithm or "bfs"

    if algorithm == "bfs":
        solver = BFSolver(initial, goal)
    elif algorithm == "dfs":
        solver == DFSolver(initial, goal)
    elif algorithm == "uniform":
        solver = UniformCostSolver(initial, goal, uniform_distance)
    elif algorithm == "astar":
        solver = AStarSolver(initial, goal, uniform_distance, heuristic)
    else:
        raise NoAlgorithmException(algorithm)
    
    solver = BFSolver(initial, goal)

    if gui:
        return run_with_snapshots(solver)
    else:
        result = solver.solve()
        return forward_solution(result)