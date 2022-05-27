from collections import deque
from io import TextIOWrapper
from itertools import chain
from typing import Iterator, List, ClassVar, Optional, Deque
from copy import deepcopy

from common.state import State

FlipArray = List[List[bool]]

class FlipState(State[FlipArray]):
    """ The class representing the state. Actual state is stored in _state """
    _state: ClassVar['FlipArray']
    expanded: ClassVar[bool] = False
    label: ClassVar[str]
    last: ClassVar['FlipState']

    w: ClassVar[int]
    h: ClassVar[int]

    def __init__(self, array: FlipArray, label: str = "", last: 'FlipState' = None) -> None:
        self._state = array
        self.label = label
        self.last = last
        
        self.w = len(self._state)
        self.h = len(self._state[0])
    
    def successor(self) -> Iterator['FlipState']:
        """ The successor states """
        for i in range(self.w):
            for j in range(self.h):
                new_state = self.copy(str(j*self.w + i + 1))
                new_state.flip(i, j)

                yield new_state
    
    def is_terminal(self, goal: 'FlipState') -> bool:
        """ Check whether current state is terminal """
        return self == goal
    
    def copy(self, new_label: str) -> 'FlipState':
        return FlipState(deepcopy(self._state), label=new_label, last=self)
    
    def flip(self, i: int, j: int):
        """ Flip around (i,j) """
        self._state[i][j] = not self._state[i][j]

        if self.h > j-1 >= 0:
            self._state[i][j-1] = not self._state[i][j-1]
        
        if self.w > i+1 >= 0:
            self._state[i+1][j] = not self._state[i+1][j]

        if self.h > j+1 >= 0:
            self._state[i][j+1] = not self._state[i][j+1]

        if self.w > i-1 >= 0:
            self._state[i-1][j] = not self._state[i-1][j]

    def __repr__(self):
        res = f""

        l = len(self.label)
        label_line = (self.label + " => ").rjust(l+4)
        empty_line = ' ' * (l+4)

        for line_num in range(self.h):
            if line_num == self.h//2:
                res += label_line
            else:
                res += empty_line
            
            for col_num in range(self.w):
                res += f"{'1' if self._state[col_num][line_num] else '0'} "
            
            res += "\n"
        
        return res
    
    def __eq__(self, __o: 'FlipState') -> bool:
        return self._state == __o._state

# Define the goal, a bit hacky

def read_from_open_file(f: TextIOWrapper) -> FlipState:
    stateArr: FlipArray = []
    with f:
        lines = f.readlines()
        for line in lines:
            stateArr.append([])
            for fl in line.strip().split():
                stateArr[-1].append(fl == '1')
    
    # Transpose:
    stateArr = list(map(list, zip(*stateArr)))
    
    return FlipState(stateArr, label='S')


def read_from_file(path: str = "input.txt") -> FlipState:
    return read_from_open_file(open(path))
    
def print_backwards(state: FlipState) -> None:
    if state is None:
        return
    
    print(state)
    print_backwards(state.last)
