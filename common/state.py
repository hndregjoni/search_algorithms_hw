from typing import ClassVar, TypeVar, Generic, Iterator, Optional, Union, Type, Any

TInnerState = TypeVar('TInnerState')
TState = TypeVar('TState', bound='State[Any]')
TGoal = Union[TState, Iterator[TState], None]

class State(Generic[TInnerState]):
    """ The class representing the state. Actual state is stored in _state """
    _state: TInnerState
    expanded: bool = False
    label: str
    last: Optional['State']

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
    
    def is_terminal(self, goal: TGoal = None) -> bool:
        """ Check whether current state is terminal """
        pass
    
    def copy(self, new_label: str) -> 'State':
        pass 