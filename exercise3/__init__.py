from common.solvers import AStarSolver, BFSolver
from common.frontiers import uniform_distance
from common.state import print_forward_solution

from .solution import *

def exercise3(argv: List[str]) -> None:
    initial, maze, goal = read_from_file()

    heuristic = hex_heuristic_to(goal)

    solver = AStarSolver(initial, goal, uniform_distance, heuristic)

    result = solver.solve()

    print_forward_solution(result)