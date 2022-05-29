from typing import ClassVar, Generic, Optional, Deque, List, Type, Any, Callable
from collections import deque

from .state import TState, TGoal, State
from .frontiers import PriorityQueeFrontier, QueueFrontier, StackFrontier, TFrontier, Frontier, zero

SolverCallback = Optional[Callable[['Solver', TState],None]]
class Solver(Generic[TState]):
    _frontier: Frontier[TState, Any]
    already_run: bool = False
    solution: Optional[TState] = None
    callback: SolverCallback = None

    def __init__(self, initial: TState, goal: TGoal, frontier: Frontier[TState, Any]) -> None:
        self._frontier = frontier

        self.initial = initial
        self.goal = goal
    
    def solve(self) -> Optional[TState]:
        assert self.already_run == False
        self.already_run = True

        # Add the initial state to the queue:
        self._frontier.add_to_frontier(self.initial)

        # Start dequeueing:
        while len(self._frontier) > 0:
            # Get item from queue:
            curr = self._frontier.peek_frontier()
            # print("====")
            # print(curr.last)
            # print(curr.last.cost if curr.last is not None else 0)
            # print("")
            # print(curr)
            # print()
            # print(curr.distance)
            # print(curr.cost)
            # print(f"Current expanded: {len(self._frontier._expanded_list)}")
            # print(f"Current frontier: {len(self._frontier._frontierColl)}")
            # print("")
            # input()

            # Check if not in expanded:
            if self._frontier.been_expanded(curr):
                self._frontier.remove_from_frontier(curr)
                continue

            # Check if it is terminal
            if curr.is_terminal(goal=self.goal):
                self.solution = curr
                self._frontier.add_to_expanded(curr)

                if self.callback is not None:
                    self.callback(self, curr)
                break
            
            # If not terminal, enqueue children:
            self._frontier.add_to_expanded(curr)

            self._frontier.remove_from_frontier(curr)

            for succ in curr.successor():
                if not self._frontier.been_expanded(succ):
                    self._frontier.add_to_frontier(succ) 

            if self.callback is not None:
                self.callback(self, curr)

        return self.solution

class AStarSolver(Generic[TState], Solver[TState]):
    """ A generic solving scheme, with g and h that make up f. """
    def __init__(self, initial: TState, goal: TGoal, g: Callable[[TState], int], h: Callable[[TState], int]) -> None:
        frontier = PriorityQueeFrontier(g, h)

        super().__init__(initial, goal, frontier)

class UniformCostSolver(Generic[TState], AStarSolver[TState]):
    """ If h = 0, we have a general Uniform Cost search, a sort of implementation of Djikstra's """
    def __init__(self, initial: TState, goal: TGoal, g: Callable[[TState], int]) -> None:
        super().__init__(initial, goal, g, zero)

class BFSolver(Generic[TState], Solver[TState]):
    """ Here we have a BFS solver """
    def __init__(self, initial: TState, goal: TGoal) -> None:
        frontier: Frontier = QueueFrontier()

        super().__init__(initial, goal, frontier)

class DFSolver(Generic[TState], Solver[TState]):
    """ Here we have a DFS solver """
    def __init__(self, initial: TState, goal: TGoal) -> None:
        frontier: Frontier = StackFrontier()

        super().__init__(initial, goal, frontier)

#
# Leaving this here just because of the sentimental values:
#

# class BFSolver(Generic[TState]):
#     initial: TState
#     _queue: Deque[TState]
#     _expanded_list: List[TState]
#     goal: TGoal
#     already_run: bool = False
#     solution: Optional[TState] = None

#     def __init__(self, initial: TState, goal: TGoal) -> None:
#         self._queue = deque()
#         self._expanded_list = []
#         self.initial = initial
#         self.goal = goal

#     def solve(self) -> Optional[TState]:
#         assert self.already_run == False
#         self.already_run = True

#         # Add the initial state to the queue:
#         self._queue.append(self.initial)

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

#             for succ in curr.successor(): # type: TState
#                 if succ not in self._queue:
#                     self._queue.append(succ)

#         return self.solution