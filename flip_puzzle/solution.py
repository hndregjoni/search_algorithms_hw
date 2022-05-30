from io import TextIOWrapper
from typing import Iterator, List, ClassVar, Optional, Deque, Type, Union, Any
from copy import deepcopy

from common.state import GridState, TGrid
from common.read_util import lines_to_int_grid

FlipArray = List[List[bool]]

class FlipState(GridState[int]):
    """ The class representing the state. Actual state is stored in _state """
    last: Optional['FlipState']
 
    def successor(self) -> Iterator['FlipState']:
        """ The successor states """
        for i in range(self.w):
            for j in range(self.h):
                new_state = self.copy(str(j*self.w + i + 1))
                new_state.flip(i, j)

                yield new_state

    def copy(self, new_label: str) -> 'FlipState':
        return FlipState(deepcopy(self._state), label=new_label, last=self)
     
    def flip(self, i: int, j: int):
        """ Flip around (i,j) """
        self._state[i][j] = 1^self._state[i][j]

        if self.h > j-1 >= 0:
            self._state[i][j-1] = 1^self._state[i][j-1]
        
        if self.w > i+1 >= 0:
            self._state[i+1][j] = 1^self._state[i+1][j]

        if self.h > j+1 >= 0:
            self._state[i][j+1] = 1^self._state[i][j+1]

        if self.w > i-1 >= 0:
            self._state[i-1][j] = 1^self._state[i-1][j]


def read_from_open_file(f: TextIOWrapper) -> FlipState:
    stateArr: TGrid[int] = []
    with f:
        lines = f.readlines()
        stateArr = lines_to_int_grid(lines) 
    
    return FlipState(stateArr, label='S')


def read_from_file(path: str = "input.txt") -> FlipState:
    return read_from_open_file(open(path)) 