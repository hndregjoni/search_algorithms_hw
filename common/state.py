from typing import ClassVar, TypeVar, Generic, Iterator, Optional, Union, Type, Any

TInnerState = TypeVar('TInnerState')
TState = TypeVar('TState', bound='State[Any]')
TGoal = Union[TState, Iterator[TState], None]

class State(Generic[TInnerState]):
    """ The class representing the state. Actual state is stored in _state """
    _state: TInnerState
    expanded: ClassVar[bool] = False
    action: ClassVar[str]
    last: Optional['State']

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