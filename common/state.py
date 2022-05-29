from typing import ClassVar, TypeVar, Generic, Iterator, Optional, Union, Type, Any, Callable, List, Tuple
from copy import deepcopy

TInnerState = TypeVar('TInnerState')
TState = TypeVar('TState', bound='State')
TGoal = Union[TState, Iterator[TState], Callable[[TState], bool], None]

class State(Generic[TInnerState]):
    """ The class representing the state. Actual state is stored in _state """
    _state: TInnerState
    expanded: bool = False
    label: str
    last: Optional['State']

    terminal: bool = False

    # To be used for holding heuristics
    distance: int = 0
    cost: int = 0

    def __lt__(self, other: Any):
        return self.cost < other.cost

    def __init__(self, inner_state: TInnerState, label: str = "", last: Optional['State'] = None) -> None:
        self._state = inner_state
        self.label = label
        self.last = last
      
    def successor(self: TState) -> Iterator['TState']:
        """ The successor states """
        pass
    
    def is_terminal(self, goal: TGoal['State[TInnerState]'] = None) -> bool:
        """ Check whether current state is terminal """
        if goal is not None:
            if isinstance(goal, State):
                if goal.terminal:
                    return True

            if callable(goal):
                return goal(self)
            
            if isinstance(goal, Iterator):
                return self in goal
            
            return self == goal 

        return False
    
    def is_solvable(self, goal: TGoal['State[TInnerState]'] = None) -> Optional[bool]:
        """ Is the current state solvable ? """
        return None
    
    def copy(self: TState, new_label: str) -> 'TState':
        pass

    def __eq__(self, __o: Any) -> bool:
        return self._state == __o._state


TGridStateCell = TypeVar('TGridStateCell')
TGrid = List[List[TGridStateCell]]

GridCoord = Tuple[int, int]

def manhattan_from(target: 'GridState[int]', memoize: bool = True) -> Callable[['GridState[int]'], int]:
    """ This creates a Manhattan distance heuristic from the given target """

    locate = target.locate
    if memoize:
        from functools import cache
        locate = cache(locate)

    def manhattan(state: 'GridState[int]') -> int:
        s = 0
        for i in range(state.w):
            for j in range(state.h):
                v = state[(i,j)]
                if v == 0: continue

                t_i, t_j = locate(v)

                s += abs(i-t_i) + abs(j-t_j)

        return s
 
    return manhattan

def off_from(target: 'GridState[int]', memoize: bool = True) -> Callable[['GridState[int]'], int]:
    """ This creates a Manhattan distance heuristic from the given target """

    locate = target.locate
    if memoize:
        from functools import cache
        locate = cache(locate)

    def off(state: 'GridState[int]') -> int:
        s = 0
        for i in range(state.w):
            for j in range(state.h):
                v = state[(i,j)]
                if v == 0: continue
                s += 1 if v != target[(i,j)] else 0

        return s
 
    return off
 

class GridState(Generic[TGridStateCell], State[TGrid[TGridStateCell]]):
    def __init__(self, array: TGrid, label: str = "", last: Optional['GridState'] = None) -> None:
        super().__init__(array, label, last)
        
        self.w = len(self._state)
        self.h = len(self._state[0])

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
                res += f"{self._state[col_num][line_num]} "
            
            res += "\n"
        
        return res

    def locate(self, val: TGridStateCell) -> GridCoord:
        for i in range(self.w):
            for j in range(self.h):
                if self._state[i][j] == val:
                    return (i, j)
        
        raise Exception(f"Value not found {val}")
    
    def __getitem__(self, key: GridCoord):
        return self._state[key[0]][key[1]]
    
    def __setitem__(self, key: GridCoord, val: TGridStateCell):
        self._state[key[0]][key[1]] = val 