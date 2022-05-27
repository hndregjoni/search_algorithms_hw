from typing import ClassVar, Generic, Optional, Deque, List, Type
from collections import deque

from .state import TState, TGoal

class BFSolver(Generic[TState]):
    initial: ClassVar[TState]
    _queue: ClassVar[Deque[TState]]
    _expanded_list: ClassVar[List[TState]]
    goal: ClassVar[TGoal]
    already_run: ClassVar[bool] = False
    solution: ClassVar[Optional[TState]] = None

    def __init__(self, initial: TState, goal: TGoal):
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

            for succ in curr.successor():
                if succ not in self._queue:
                    self._queue.append(succ)

        return self.solution