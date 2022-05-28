from copy import deepcopy
from typing import ClassVar, TypeVar, Generic, Iterator, Optional, Union, Type, Any, Callable, List, cast

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
    
    def copy(self: TState, new_label: str) -> 'TState':
        pass


TGridStateCell = TypeVar('TGridStateCell')
TGrid = List[List[TGridStateCell]]

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
                res += f"{'1' if self._state[col_num][line_num] else '0'} "
            
            res += "\n"
        
        return res
    
    def __eq__(self, __o: Any) -> bool:
        return self._state == __o._state