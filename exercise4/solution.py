from io import TextIOWrapper
from tkinter import W
from typing import Sequence, Any, List, Optional, Iterator, Tuple

from copy import deepcopy
from dataclasses import dataclass
from enum import Enum

from common.state import GridCoord, TGrid, State, Optional

Axis = Enum('Axis', 'H V')

@dataclass
class Tile:
    index: int

    axis: Axis
    length: int
    coord: GridCoord
    
    # If V goes bottom up
    # def part_iterator(self) -> Iterator[GridCoord]:
    #     y, x = self.coord

    #     if self.axis == Axis.V:
    #         # Vertical
    #         # Start bottom, go up
    #         for i in range(self.length):
    #             yield (y-i, x)
    #     elif self.axis == Axis.H:
    #         # Horizontal
    #         # Start left, go right
    #         for i in range(self.length):
    #             yield (y, x+i)

    # If V goes top bottom
    def part_iterator(self) -> Iterator[GridCoord]:
        y, x = self.coord

        if self.axis == Axis.V:
            # Vertical
            # Start bottom, go up
            for i in range(self.length):
                yield (y+i, x)
        elif self.axis == Axis.H:
            # Horizontal
            # Start left, go right
            for i in range(self.length):
                yield (y, x+i)

TBoard = TGrid[Optional[int]]

class UnblockState(State[List[Tile]]):
    last: Optional['UnblockState']
    _board: TBoard

    w: int
    h: int

    def __init__(self, inner_state: List[Tile], w: int = 6, h: int = 6, label: str = "", last: Optional['State'] = None, plot: bool = True) -> None:
        super().__init__(inner_state, label, last)

        self.w = w
        self.h = h

        if plot:
            self.plot_board()
    
    def successor(self) -> Iterator['UnblockState']:
        for i, tile in enumerate(self._state):
            # Check whether we have a clear path towards the exit, if we do, then exit:
            if tile.index == 0:
                y, x = tile.coord
                path_clear = True
                for path_tile in self._board[y][x+tile.length:self.w]:
                    if path_tile is not None and path_tile != 0:
                        path_clear = False
                        break

                if path_clear:
                    new_state = self.copy(f"{y} {x} {self.w-x} R") 
                    new_state._state[0].coord = (y, self.w)
                    new_state.plot_board()
                    yield new_state


            for legit_move in self.iterate_tile_moves(tile):
                # Now we have a legitimate move, clone the tiles, and change this specific one
                orig_coord, distance, direction, new_coord = legit_move

                new_state = self.copy(f"{orig_coord[0]} {orig_coord[1]} {distance} {direction}")
                new_state._state[i].coord = new_coord
                new_state.plot_board()

                yield new_state
    
    def copy(self, new_label: str) -> 'UnblockState':
        return UnblockState(deepcopy(self._state), w=self.w, h=self.h, label=new_label, last=self, plot=False)

    # If V goes bottom up
    # def iterate_tile_moves(self, tile: Tile) -> Iterator[Tuple[GridCoord, int, str, GridCoord]]:
    #     """ Tries going in the positive direction until it stops, then in the negative one """
    #     y, x = tile.coord
    #     c: GridCoord

    #     # Positive
    #     for d in range(max(self.w, self.h)):
    #         if tile.axis == Axis.V:
    #             # Go down
    #             c = (y+d+1, x)
    #             if not self.within_and_empty(c):
    #                 break
    #             else:
    #                 yield tile.coord, d, 'D', (y+d+1, x)
            
    #         if tile.axis == Axis.H:
    #             # Go right
    #             c = (y, x+tile.length+d) # This is actually x + tile.length-1 + d + 1

    #             if not self.within_and_empty(c):
    #                 break
    #             else:
    #                 yield tile.coord, d, 'R', (y, x+d+1)
    #     # Negative
    #     for d in range(max(self.w, self.h)):
    #         if tile.axis == Axis.V:
    #             # Go up
    #             c = (y-tile.length-d, x) # Similarly
    #             if not self.within_and_empty(c):
    #                 break
    #             else:
    #                 yield tile.coord, d, 'U', (y-d-1, x)
            
    #         if tile.axis == Axis.H:
    #             # Go left
    #             c = (y, x-d-1) 

    #             if not self.within_and_empty(c):
    #                 break
    #             else:
    #                 yield tile.coord, d, 'L', (y, x-d-1)

    # If V goes top bottom
    def iterate_tile_moves(self, tile: Tile) -> Iterator[Tuple[GridCoord, int, str, GridCoord]]:
        """ Tries going in the positive direction until it stops, then in the negative one """
        y, x = tile.coord
        c: GridCoord


        # # We don't want to stop the main tile from the end
        # should_break = lambda c: (tile.index == 0 and not (self.empty(c))) \
        #     or (tile.index != 0 and not self.within_and_empty(c))
        should_break = lambda c: not self.within_and_empty(c)

        # Positive
        for d in range(max(self.w, self.h)):
            if tile.axis == Axis.V:
                # Go down
                c = (y+tile.length+d, x)
                if should_break(c):
                    break
                else:
                    yield tile.coord, d+1, 'D', (y+d+1, x)
            
            if tile.axis == Axis.H:
                # Go right
                c = (y, x+tile.length+d) # This is actually x + tile.length-1 + d + 1

                if should_break(c):
                    break
                else:
                    yield tile.coord, d+1, 'R', (y, x+d+1)
        # Negative
        for d in range(max(self.w, self.h)):
            if tile.axis == Axis.V:
                # Go up
                c = (y-d-1, x) 
                if should_break(c):
                    break
                else:
                    yield tile.coord, d+1, 'U', (y-d-1, x)
            
            if tile.axis == Axis.H:
                # Go left
                c = (y, x-d-1) 

                if should_break(c):
                    break
                else:
                    yield tile.coord, d+1, 'L', (y, x-d-1)

    def plot_tile(self, tile: Tile) -> None:
        for part_coord in tile.part_iterator():
            if tile.index != 0 and not self.within(part_coord):
                raise(Exception(f"Tile {tile.index} out of bounds"))

            if not self.empty(part_coord):
                raise(Exception(f"Tile overlap at {part_coord} between attempted {tile.index} and {self[part_coord]}!"))

            if part_coord[1] < self.w:
                self[part_coord] = tile.index

    def within(self, coord: GridCoord) -> bool:
        y, x = coord

        return 0 <= y < self.h \
            and 0 <= x < self.w

    def pp_board(self) -> str:
        res = ""
        for line in self._board:
            for col in line:
                res += str(col).rjust(5)
            res += "\n"
        
        return res
    
    def __repr__(self) -> str:
        return self.label + "\n" + self.pp_board()
    
    def empty(self, coord: GridCoord) -> bool:
        if not self.within(coord): return True
        return self[coord] is None
    
    def within_and_empty(self, coord: GridCoord) -> bool:
        return self.within(coord) and self.empty(coord)
    
    def empty_board(self) -> TBoard:
        _board: TBoard = []
        for j in range(self.h):
            _board.append([])
            for i in range(self.w):
                _board[-1].append(None)
        
        return _board

    def plot_board(self) -> None:
        self._board = self.empty_board()

        for tile in self._state:
            self.plot_tile(tile)
    
    def __getitem__(self, key: GridCoord) -> Optional[int]:
        return self._board[key[0]][key[1]]
    
    def __setitem__(self, key: GridCoord, val: Optional[int]) -> None:
        self._board[key[0]][key[1]] = val

def read_from_open_file(f: TextIOWrapper) -> UnblockState:
    tiles: List[Tile] = []

    with f:
        lines = f.readlines()
        tiles_cnt = int(lines[0])
        if tiles_cnt > 0:
            for i, line in enumerate(lines[1:]):
                _axis, _y, _x, _length = line.split()
                y, x = int(_y), int(_x)
                axis = Axis[_axis]
                length = int(_length)
                
                tiles.append(Tile(i, axis, length, (y-1, x-1)))
    
    return UnblockState(tiles, label="S")


def read_from_file(path: str = "exercise4/input3.txt") -> UnblockState:
    return read_from_open_file(open(path))