from typing import ClassVar, Generic, Optional, Deque, List, Type
from collections import deque

from .state import TState, TGoal, State
# from .frontiers import TFrontier

# class Solver(Generic[TState, TFrontier]):
#     _frontier: ClassVar[TFrontier]
#     already_run: bool = False

#     def __init__(self, initial: TState, goal: TGoal, frontier: TFrontier) -> None:
#         self._frontier = frontier

#         self.initial = initial
#         self.goal = goal
    
#     def solve(self) -> Optional[TState]:
#         assert self.already_run == False
#         self.already_run = True

#         # Add the initial state to the queue:
#         self._frontier.add_to_frontier(self.initial)

#         # Start dequeueing:
#         while len(self._queue) > 0:
#             # Get item from queue:
#             curr = self._queue.popleft()

#             # Check if not in expanded:
#             if curr in self._expanded_list:
#                 continue

#             # Check if it is terminal
#             if curr.is_terminal(goal=self.goal):
#                 self.solution = curr
#                 self._expanded_list.append(curr)
#                 break
            
#             # If not terminal, enqueue children:
#             self._expanded_list.append(curr)

#             for succ in curr.successor():
#                 if succ not in self._queue:
#                     self._queue.append(succ)

#         return self.solution

class BFSolver(Generic[TState]):
    initial: TState
    _queue: Deque[TState]
    _expanded_list: List[TState]
    goal: TGoal
    already_run: bool = False
    solution: Optional[TState] = None

    def __init__(self, initial: TState, goal: TGoal) -> None:
        self._queue = deque()
        self._expanded_list = []
        self.initial = initial
        self.goal = goal

    def solve(self) -> Optional[TState]:
        assert self.already_run == False
        self.already_run = True

        # Add the initial state to the queue:
        self._queue.append(self.initial)

        # Start dequeueing:
        while len(self._queue) > 0:
            # Get item from queue:
            curr = self._queue.popleft()

            # Check if not in expanded:
            if curr in self._expanded_list:
                continue

            # Check if it is terminal
            if curr.is_terminal(goal=self.goal):
                self.solution = curr
                self._expanded_list.append(curr)
                break
            
            # If not terminal, enqueue children:
            self._expanded_list.append(curr)

            for succ in curr.successor(): # type: TState
                if succ not in self._queue:
                    self._queue.append(succ)

        return self.solution