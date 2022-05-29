from typing import Tuple, Optional, List, cast
# type: ignore
from PIL.Image import Image

from common.solvers import AStarSolver, BFSolver, Solver
from common.frontiers import uniform_distance
from common.state import print_forward_solution

from .solution import *
from .graphics import draw_hexgrid_state

def is_ancestor(child: HexMazeState, alleged: HexPosition):
    """ Checks whether a state is ancestor of another """
    if child is None:
        return False

    if child.last == alleged:
        return True
    
    return is_ancestor(child.last, alleged)

def run_with_snapshots(solver: Solver[HexMazeState]) -> Tuple[Optional[HexMazeState], List[Image]]:
    images: List[Image] = []

    def callback(_solver: Solver[HexMazeState], state: HexMazeState):
        def color_picker(row: int, col: int) -> str:
            # Ok, it got deep.
            hex_pos: HexPosition = cast(HexPosition, (row, col))

            # First check if head:
            if hex_pos == state:
                return "#698A03"
            # Or check if begin:
            elif hex_pos == _solver.initial._state:
                # print("Here1")
                return "#3063C6"
            # Or goal:
            elif isinstance(_solver.goal, HexMazeState) and hex_pos == _solver.goal._state:
                # print("Here2")
                return "#F60000"
            # Or in paht
            elif is_ancestor(state, hex_pos):
                return "#B5E61D"
            # Or expanded
            elif hex_pos in _solver._frontier._expanded_list:
                # print("Here4")
                return "#C9D996"
            # Or in frontied
            elif hex_pos in _solver._frontier._frontierColl:
                # print("Here3")
                return "#DFFC83"
            # Or wall
            elif state.maze[row][col] == Tile.WALL:
                # print("Here5")
                # print("WALL!")
                return "#000000"
            # Empty
            else:
                # print("Here6")
                return "#ffffff" 

        img = draw_hexgrid_state(state, decide_fill=color_picker)
        images.append(img)

    
    solver.callback = callback

    result = solver.solve()

    return result, images

def exercise3(argv: List[str]) -> None:
    initial, maze, goal = read_from_file()

    heuristic = hex_heuristic_to(goal)

    solver = AStarSolver(initial, goal, uniform_distance, heuristic)

    result, images = run_with_snapshots(solver)

    return result, images

    # result = solver.solve()

    # print_forward_solution(result)
