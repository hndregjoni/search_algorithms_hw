from common.solvers import BFSolver
from .solution import *

def goal(state: UnblockState) -> bool:
    """ This target assumes that the 0th tile is the main one 
    and also that it's always horizontal"""
    
    return state._state[0].coord[1] >= state.w

def exercise4(argv: List[str]) -> None:
    initial = read_from_file()

    solver = BFSolver(initial, goal)

    result = solver.solve()

    print_backwards(result)