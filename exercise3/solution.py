from typing import NewType, List, Optional, Iterator, Tuple, cast, Callable, Any

from io import TextIOWrapper
from copy import deepcopy
from enum import Enum
from common.read_util import lines_to_int_grid, read_int_twople

from common.state import State, GridCoord

Tile = Enum('Tile', 'WALL EMPTY')


HexGrid = List[List[Tile]]
HexPosition = NewType('HexPosition', GridCoord)


class HexMazeState(State[HexPosition]):
    """ 15-puzzle State """
    last: Optional['HexMazeState']
    maze: HexGrid

    w: int
    h: int

    def __init__(self, inner_state: HexPosition, maze: HexGrid, label: str = "", last: Optional['State'] = None) -> None:
        super().__init__(inner_state, label, last)

        self.maze = maze

        self.h = len(self.maze)
        self.w = len(self.maze[0])

    def successor(self) -> Iterator['HexMazeState']:
        coords: List[GridCoord]

        i, j = self._state

        # Different behaviour whether current row is even or odd        
        if i % 2 == 0:
            # If even, the adjecent rows will have indices: (j, j+1)
            coords = [
                (i-1, j+1),
                (i-1, j  ),
                (i  , j+1),
                (i+1, j  ),
                (i+1, j+1),
                (i  , j-1)
            ]
        else:
            # If odd, the adjecent rows will have indices: (j-1, j)
            coords = [
                (i-1, j-1),
                (i-1, j  ),
                (i  , j+1),
                (i+1, j  ),
                (i+1, j-1),
                (i  , j-1)
            ]
        
        for coord in filter(self.within, coords):
            if not self.empty_tile(coord): continue

            new_state = self.copy(f"{coord[0]} {coord[1]}")
            new_state._state = cast(HexPosition, coord)

            yield new_state
    
    @staticmethod
    def grid_distance(coord1: HexPosition, coord2: HexPosition) -> int:
        dx: int
        dy: int
        dx = coord1[0] - coord1[0]
        dy = (coord1[0]//2+coord1[1]) - (coord2[0]//2 + coord2[1])

        # Checking sign
        if (dx*dy >= 0):
            return max(abs(dx), abs(dy))
        else:
            return abs(dx) + abs(dy)
    
    def within(self, coord: GridCoord) -> bool:
        i, j = coord

        return 0 <= i < self.h \
            and 0 <= j < self.w

    def empty_tile(self, coord: GridCoord) -> bool:
        return self[coord] == Tile.EMPTY

    def __repr__(self) -> str:
        return str(self._state)
     
    def __getitem__(self, key: GridCoord) -> Tile:
        return self.maze[key[0]][key[1]]
    
    def __setitem__(self, key: GridCoord, val: Tile) -> None:
        self.maze[key[0]][key[1]] = val
    
    def __eq__(self, __o: Any) -> bool:
        if (isinstance(__o, tuple)):
            return self._state == __o
        return super().__eq__(__o)
    
    def copy(self, new_label: str) -> 'HexMazeState':
        return HexMazeState(deepcopy(self._state), self.maze, new_label, self)


def empty_maze(w: int, h: int) -> HexGrid:
    maze: HexGrid = []

    for j in range(h):
        maze.append([])
        for j in range(w):
            maze[-1].append(Tile.EMPTY)

    return maze


def hex_heuristic_to(goal: HexMazeState) -> Callable[[HexMazeState], int]:
    def heuristic(state: HexMazeState) -> int:
        return HexMazeState.grid_distance(state._state, goal._state)

    return heuristic

def read_from_open_file(f: TextIOWrapper) -> Tuple[HexMazeState, HexGrid, HexMazeState]:
    maze: HexGrid

    with f:
        lines = f.readlines()
        dims = lines[0]
        w, h = read_int_twople(dims)

        maze = empty_maze(w, h)

        start = lines[1]
        start_coord: HexPosition = cast(HexPosition, read_int_twople(start))
        
        goal = lines[2]
        goal_coord: HexPosition = cast(HexPosition, read_int_twople(goal))

        walls = int(lines[3])


        if walls > 0:
            for wall in lines[4:]:
                i, j = read_int_twople(wall)
                maze[i][j] = Tile.WALL

        return HexMazeState(start_coord, maze, "S"), \
            maze, \
            HexMazeState(goal_coord, maze, "G")


def read_from_file(path: str = "exercise3/input.txt") -> Tuple[HexMazeState, HexGrid, HexMazeState]:
    return read_from_open_file(open(path))