from typing import Generic, Collection, TypeVar, ClassVar, List, Deque, Optional, Type, Any, Deque
from collections import deque

from .state import TState, State

TFrontierCollection = TypeVar('TFrontierCollection', bound=Collection)

TFrontier = TypeVar('TFrontier', bound='Frontier[State, Collection[State]]')

class Frontier(Generic[TState, TFrontierCollection]):
    _frontierColl: TFrontierCollection
    _expanded_list: List[TState]

    def __init__(self, frontier: TFrontierCollection):
        self._expanded_list = list()
        self._frontierColl = frontier

    def in_frontier(self, state: TState) -> bool:
        return state in self._frontierColl
    
    def been_expanded(self, state: TState) -> bool:
        return state in self._expanded_list
    
    def add_to_frontier(self, state: TState) -> None:
        pass

    def add_to_expanded(self, state: TState) -> None:
        self._expanded_list.append(state)

    def __len__(self):
        return len(self._frontierColl)

    def peek_frontier(self) -> TState:
        pass
    
    def remove_from_frontier(self, state: Optional[TState]) -> None:
        pass


class QueueFrontier(Generic[TState], Frontier[TState, Deque[TState]]):
    def __init__(self):
        super().__init__(deque())
    
    def add_to_frontier(self, state: TState) -> None:
        self._frontierColl.append(state)
    
    def peek_frontier(self) -> TState:
        return self._frontierColl[0]
    
    def remove_from_frontier(self, _: Optional[TState] = None) -> None:
        # Simply pop
        self._frontierColl.popleft()
        

class PriorityQueueFrontier:
    def __init__(self):
        pass

class StackFrontier(Generic[TState], Frontier[TState, Deque[TState]]):
    def __init__(self):
        super().__init__(deque())
    
    def add_to_frontier(self, state: TState) -> None:
        self._frontierColl.appendleft(state)
    
    def peek_frontier(self) -> TState:
        return self._frontierColl[0]
    
    def remove_from_frontier(self, state: Optional[TState] = None) -> None:
        # Simply pop
        if state is not None:
            k: int
            found: int
            v: TState
            for k, v in enumerate(self._frontierColl): 
                if v is state:
                    found = k
            
            del self._frontierColl[found]