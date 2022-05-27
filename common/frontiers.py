# from typing import Generic, Collection, TypeVar, ClassVar, List, Deque, Optional
# from collections import deque

# from state import TState

# TFrontierCollection = TypeVar('TFrontierCollection', bound=Collection)

# TFrontier = TypeVar('TFrontier', bound='Frontier[TFrontierCollection]')

# class Frontier(Generic[TState, TFrontierCollection]):
#     _frontierColl: ClassVar[TFrontierCollection]
#     _expanded_list: ClassVar[List[TState]]

#     def __init__(self, frontier: TFrontierCollection[TState]):
#         self._expanded_list = list()
#         self._frontierColl = frontier

#     def in_frontier(self, state: TState) -> bool:
#         return state in self._frontierColl
    
#     def been_expanded(self, state: TState) -> bool:
#         return state in self._expanded_list
    
#     def add_to_frontier(self, state: TState) -> None:
#         pass

#     def peek_frontier(self) -> TState:
#         pass
    
#     def remove_from_frontier(self, state: Optional[TState]) -> None:
#         pass


# class QueueFrontier(Frontier[Generic[TState], Deque[TState]]):

#     def __init__(self):
#         super().__init__(deque())
    
#     def add_to_frontier(self, state: TState) -> None:
#         self._frontierColl.append(state)
    
#     def peek_frontier(self) -> TState:
#         return self._frontierColl[0]
    
#     def remove_from_frontier(self, _: Optional[TState] = None) -> None:
#         # Simply pop
#         self._frontierColl.popleft()
        

# class PriorityQueueFrontier:
#     pass

# class StackFrontier:
#     pass