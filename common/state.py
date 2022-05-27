from typing import ClassVar, TypeVar, Generic, Iterator, Optional, Union

TInnerState = TypeVar('TInnerState')
TState = TypeVar('TState', bound='State')
TGoal = Union[TState, Iterator[TState], None]

class State(Generic[TInnerState]):
    """ The class representing the state. Actual state is stored in _state """
    _state: ClassVar[TInnerState]
    expanded: ClassVar[bool] = False
    action: ClassVar[str]
    last: ClassVar[TState]

    w: ClassVar[int]
    h: ClassVar[int]

    def __init__(self, inner_state: TInnerState, label: str = "", last: TState = None) -> None:
        self._state = inner_state
        self.label = label
        self.last = last
      
    def successor(self) -> Iterator[TState]:
        """ The successor states """
        for i in range(self.w):
            for j in range(self.h):
                new_state = self.copy(str(j*self.w + i + 1))
                new_state.flip(i, j)

                yield new_state
    
    def is_terminal(self, goal: TGoal = None) -> bool:
        """ Check whether current state is terminal """
        pass
    
    def copy(self, new_label: str) -> TState:
        pass 