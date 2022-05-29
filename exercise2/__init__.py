from typing import List

from common.state import manhattan_from, off_from, print_forward_solution

from .solution import *

from common.solvers import AStarSolver, BFSolver, Solver, UniformCostSolver
from common.frontiers import PriorityQueeFrontier, QueueFrontier, StackFrontier, uniform_distance

# This is transposed, to allow for [i][j] coordinate
goal = FifteenState(
    [[1 , 5 , 9 , 13],
     [2 , 6 , 10, 14],
     [3 , 7 , 11, 15],
     [4 , 8 , 12, 0 ]],
    "S"
)

def is_solvable(state: FifteenState, w: int = 4, h: int = 4):
    """ This checks whether the state can be turned into the standard goal with legal moves: """
    if w != 4 or h != 4:
        raise Exception("The is_solvable method only works for the most trivial check (4x4 and goal is standard)")

    inversions = state.get_inversions()
    even_inversions = inversions % 2 == 0
    odd_inversions = not even_inversions

    if w % 2 == 0:
        return even_inversions
    else:
        _, blank_row = state.locate_blank()
        blank_row_bottom = h - blank_row

        if blank_row_bottom % 2 == 1:
            return even_inversions
        else:
            return odd_inversions

manhattan_heuristic = manhattan_from(goal)
off_heuristic = off_from(goal)
# def quicker_manhattan_heuristic(state: GridState[int]) -> int:
#     f

def exercise2(argv: List[str]):
    initial = read_from_file("exercise2/input.txt")

    if not is_solvable(initial):
        raise Exception("There is no solution for the given input.")

    solver = AStarSolver(initial, goal, uniform_distance, manhattan_heuristic)

    result = solver.solve()

    print_forward_solution(result)