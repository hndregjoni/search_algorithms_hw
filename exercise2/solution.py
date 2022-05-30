from io import TextIOWrapper
from typing import Optional, Iterator

from copy import deepcopy
from common.read_util import lines_to_int_grid

from common.state import GridState, TGrid, GridCoord, TGoal

class FifteenState(GridState[int]):
    """ 15-puzzle State """
    last: Optional['FifteenState']

    blank_pos: GridCoord

    def __init__(self, array: TGrid[int], label: str = "", last: Optional['FifteenState'] = None) -> None:
        super().__init__(array, label, last)

        self.blank_pos = self.locate_blank()

    def successor(self) -> Iterator['FifteenState']:
        """ The successor states """
        blank_i: int
        blank_j: int

        blank_i, blank_j = self.blank_pos

        # North
        if blank_j > 0:
            north_coord = (blank_i, blank_j-1)
            north_state = self.copy(str(self[north_coord]))
            north_state.swap_blank(north_coord)
            yield north_state
        
        # East
        if blank_i < self.w-1:
            east_coord = (blank_i+1, blank_j)
            east_state = self.copy(str(self[east_coord]))
            east_state.swap_blank(east_coord)
            yield east_state

        # South
        if blank_j < self.h-1:
            south_coord = (blank_i, blank_j+1)
            south_state = self.copy(str(self[south_coord]))
            south_state.swap_blank(south_coord)
            yield south_state
        
        # West
        if blank_i > 0:
            west_coord = (blank_i-1, blank_j)
            west_state = self.copy(str(self[west_coord]))
            west_state.swap_blank(west_coord)
            yield west_state

    def copy(self, new_label: str) -> 'FifteenState':
        return FifteenState(deepcopy(self._state), label=new_label, last=self)

    def swap_blank(self, target: GridCoord):
        self[self.blank_pos] = self[target]
        self[target] = 0
        self.blank_pos = target

    def locate_blank(self) -> GridCoord:
        return self.locate(0)
    
    def get_inversions(self) -> int:
        inversions = 0

        N = self.w * self.h

        for k in range(N):
            k_j = k // self.w
            k_i = k % self.w

            at_k = self._state[k_i][k_j]

            for l in range(k+1, N):
                l_j = l // self.w
                l_i = l % self.h

                at_l = self._state[l_i][l_j]

                if at_k != 0 and at_l != 0 and at_k > at_l:
                    inversions += 1
        
        return inversions

def read_from_open_file(f: TextIOWrapper) -> FifteenState:
    stateArr: TGrid[int] = []
    with f:
        lines = f.readlines()
        stateArr = lines_to_int_grid(lines) 
    
    return FifteenState(stateArr, label='S')


def read_from_file(path: str = "input.txt") -> FifteenState:
    return read_from_open_file(open(path))