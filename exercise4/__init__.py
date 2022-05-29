from typing import List, Tuple, Optional

from PIL.Image import Image

from common.solvers import BFSolver, Solver
from common.state import forward_solution, print_forward_solution
from .solution import *
from .graphics import draw_unblock_state

def run_with_snapshots(solver: Solver[UnblockState]) -> Tuple[Optional[UnblockState], List[Image]]:
    images: List[Image] = []

    result = solver.solve()

    steps = forward_solution(result)
    for step in steps:
        images.append(draw_unblock_state(step))
    
    return result, images

def goal(state: UnblockState) -> bool:
    """ This target assumes that the 0th tile is the main one 
    and also that it's always horizontal"""
    
    return state._state[0].coord[1] >= state.w

def exercise4(argv: List[str]):
    initial = read_from_file()

    solver = BFSolver(initial, goal)

    # result = solver.solve()

    # print_forward_solution(result)

    return run_with_snapshots(solver)