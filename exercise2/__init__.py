from typing import List

from common.state import manhattan_from, off_from

from .solution import *

from common.solvers import AStarSolver, BFSolver, Solver, UniformCostSolver
from common.frontiers import PriorityQueeFrontier, QueueFrontier, StackFrontier, uniform_distance

goal = FifteenState(
    [[1 , 5 , 9 , 13],
     [2 , 6 , 10, 14],
     [3 , 7 , 11, 15],
     [4 , 8 , 12, 0 ]],
    "S"
)

manhattan_heuristic = manhattan_from(goal)
off_heuristic = off_from(goal)
# def quicker_manhattan_heuristic(state: GridState[int]) -> int:
#     f

def exercise2(argv: List[str]):
    initial = read_from_file("exercise2/input.txt")

    solver = AStarSolver(initial, goal, uniform_distance, off_heuristic)

    result = solver.solve()

    print_backwards(result)