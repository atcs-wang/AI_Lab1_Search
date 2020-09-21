# Lab 1: 
# Name(s): Mr. Wang
# Email(s): matwan@bergen.org

from __future__ import annotations
from typing import List, Collection, Tuple, Callable, Optional, Union, Set, Dict
import random
from collections import deque
# from priorityqueue import priorityqueue
import heapq
from search_problem import StateNode, Action


INF = float('inf')

"""
Immutable collection of information that the GUI uses
to update itself upon callback from the search algorithms.
"""
# class GUI_Callback_Info(NamedTuple):
#     extended_state : Optional[StateNode] = None
#     total_enqueues : Optional[int] = None
#     total_extends : Optional[int] = None
#     state_cost_heuristic : Optional[float] = None

#### Lab 1, Part 1a: Uninformed Search #################################################

class GoalSearchAgent():
    """
    Abstract class for Goal Search Agents.
    """
    frontier : Collection
    total_extends : int 
    total_enqueues : int

    """ __init__, enqueue, and dequeue be overridden by strategy subclasses (RandomWalk, RandomSearch, DFS, BFS, UCS, Greedy, and AStar)"""

    def __init__(self, *args, **kwargs):
        """Initialize self.total_extends and self.total_enqueues to 0s. 
        Subclasses should initialize an empty frontier that enqueue() and dequeue() operate on.
        """
        super().__init__()
        self.total_extends = 0
        self.total_enqueues = 0

    def enqueue(self, state: StateNode, cutoff: Union[int, float] = INF):
        """ Add the state to the frontier, unless some property (e.g. depth/path cost) exceeds the cutoff """
        # Subclasses will override and implement.
        raise NotImplementedError
        
    def dequeue(self) -> StateNode:
        """ Choose, remove, and return a state from the frontier """
        # Subclasses will override and implement.
        raise NotImplementedError

    """ search to be implemented by mixin algorithms (i.e. TreeSearch, GraphSearch )"""

    def search(self, 
            initial_state : StateNode, 
            gui_callback_fn : Callable[[StateNode],bool] = lambda : False,
            cutoff : Union[int, float] = INF 
            ) -> Optional[StateNode]:
        """ To be overridden by algorithm subclasses (TreeSearchAgent, GraphSearchAgent, AnytimeSearchAlgorithmMixin)
        """
        raise NotImplementedError


class RandomSearch(GoalSearchAgent):
    """ Partial class representing the Random Search strategy.
    Needs to be subclassed (multiple inheritance) with a mixin that
    that implements search (i.e. TreeSearchAgent or GraphSearchAgent)
    """
    frontier : List[StateNode]
    
    def __init__(self, *args, **kwargs):
        """ Create an empty frontier queue, 
        and initialize self.total_extends and self.total_enqueues to 0s. 
        """
        super().__init__(*args, **kwargs) # pass any unused parameters to any superclasses
        self.frontier = []

        
    def enqueue(self, state: StateNode, cutoff: Union[int, float] = INF):
        """ Add the state to the frontier, unless depth exceeds the cutoff """
        if state.depth < cutoff:
            self.frontier.append(state)

        
    def dequeue(self) -> StateNode:
        """  Choose, remove, and return a random state from the frontier."""
        s = random.choice(self.frontier)
        self.frontier.remove(s)
        return s



class TreeSearchAlgorithmMixin(GoalSearchAgent):
    """
    Mixin class for the tree search algorithm (without backtracking).

    Needs to be mixed in with a "strategy" subclass of GoalSearchAgent that
    implements the other methods (i.e. RandomSearch, DFS, BFS, UCS, etc.)
    """
    def search(self, 
            initial_state : StateNode, 
            gui_callback_fn : Callable[[StateNode],bool] = lambda : False,
            cutoff : Union[int, float] = INF 
            ) -> Optional[StateNode]:
        """ Perform a search from the initial_state, which constitutes the initial frontier.
        Repeat:
        1) dequeue a state
        2) If the state
        3) Extend the state: enqueue all its neighboring states. (with cutoff) 
                This search should implement the "avoid backtracking" optimization 
                (When extending, do not enqueue direct parents)
        This is a "tree search" - it allows re-enqueueing or re-extending of the same state, multiple times.
        """
        self.enqueue(initial_state)
        while self.frontier: #while frontier is not empty (returns False when empty)
            ext_node = self.dequeue()       # pop from queue and extend

            if ext_node.is_goal_state():
                return ext_node 

            if(gui_callback_fn(ext_node)):
                break

            self.total_extends += 1

            for neighbor in ext_node.generate_neighbor_states():
                if neighbor != ext_node.parent: # This is the no-backtracking check
                    self.enqueue(neighbor, cutoff)
                    self.total_enqueues += 1

        return None # if frontier ever empties without finding the goal, search has failed


class DepthFirstSearch(GoalSearchAgent):
    """ Partial class representing the Depth First Search strategy.
    Needs to be subclassed (multiple inheritance) with a mixin that
    that implements search (i.e. TreeSearchAgent or GraphSearchAgent)

    DFS is implemented with a LIFO queue. A list is an efficient one. 
    """
    frontier : List[StateNode]
    
    def __init__(self, *args, **kwargs):
        """ Create an empty frontier queue, 
        and initialize self.total_extends and self.total_enqueues to 0s. 
        """
        super().__init__(*args, **kwargs)
        self.frontier = []

        
    def enqueue(self, state: StateNode, cutoff: Union[int, float] = INF):
        """ Add the state to the frontier, unless depth exceeds the cutoff """
        if state.depth < cutoff:
            self.frontier.append(state)

        
    def dequeue(self) -> StateNode:
        """  Choose, remove, and return the MOST RECENTLY ADDED state from the frontier."""
        return self.frontier.pop()

class BreadthFirstSearch(GoalSearchAgent):
    """ Partial class representing the Breadth First Search strategy.
    Needs to be subclassed (multiple inheritance) with a mixin that
    that implements a search algorithm (i.e. TreeSearchAgent or GraphSearchAgent)


    BFS is implemented with a FIFO queue. The deque data structure is an efficient one.
    """
    frontier : deque[StateNode]
    
    def __init__(self, *args, **kwargs):
        """ Create an empty frontier queue, 
        and initialize self.total_extends and self.total_enqueues to 0s. 
        """
        super().__init__(*args, **kwargs)
        self.frontier = deque()

        
    def enqueue(self, state: StateNode, cutoff: Union[int, float] = INF):
        """ Add the state to the frontier, unless depth exceeds the cutoff """
        if state.depth < cutoff:
            self.frontier.append(state)

        
    def dequeue(self) -> StateNode:
        """  Choose, remove, and return the LEAST RECENTLY ADDED state from the frontier."""
        return self.frontier.popleft()


class UniformCostSearch(GoalSearchAgent):
    """ Partial class representing the Uniform Cost Search strategy.
    Needs to be subclassed (multiple inheritance) with a mixin that
    that implements a search algorithm (i.e. TreeSearchAgent or GraphSearchAgent)

    UCS is implemented with a priority queue. 
    The heapq library helps use a list as a efficient heap.
    heapq.heappush and heapq.heappop are key.
    Since states aren't ordered, the elements of the list-heap should be 
    tuples; the heap is ordered by the first element.
    """
    frontier : List[Tuple[float, StateNode]]
    
    def __init__(self,*args, **kwargs):
        """ Create an empty frontier queue, 
        and initialize self.total_extends and self.total_enqueues to 0s. 
        """
        super().__init__(*args, **kwargs)
        self.frontier = []

        
    def enqueue(self, state: StateNode, cutoff: Union[int, float] = INF):
        """ Add the state to the frontier, unless path COST exceeds the cutoff """
        if state.path_cost < cutoff:
            heapq.heappush(self.frontier, (state.path_cost, state))

        
    def dequeue(self) -> StateNode:
        """  Choose, remove, and return the state with LOWEST PATH COST from the frontier."""
        return heapq.heappop(self.frontier)[1]

class GraphSearchAlgorithmMixin(GoalSearchAgent):
    """
    Mixin class for the graph search (extended state filter) algorithm.
    
    Needs to be mixed in with a "strategy" subclass of GoalSearchAgent that
    implements the other methods (i.e. RandomSearch, DFS, BFS, UCS, etc.)
    """
    def search(self, 
            initial_state : StateNode, 
            gui_callback_fn : Callable[[StateNode],bool] = lambda : False,
            cutoff : Union[int, float] = INF 
            ) -> Optional[StateNode]:
        """ Perform a search from the initial_state, which constitutes the initial frontier.
        Repeat:
        1) dequeue a state
        2) If the state
        3) Extend the state: enqueue all its neighboring states. (with cutoff) 
                This search should implement the "avoid backtracking" optimization 
                (When extending, do not enqueue direct parents)
        This is a "tree search" - it allows re-enqueueing or re-extending of the same state, multiple times.
        """
        ext_filter : Set[StateNode] = set() # Create an empty extended state filter

        self.enqueue(initial_state)
        while self.frontier: 
            ext_node = self.dequeue()       

            # When dequeueing, check if previously extended.
            if ext_node in ext_filter:
                continue

            # Add the (about to be) extended state to the filter
            ext_filter.add(ext_node)

            if ext_node.is_goal_state():
                return ext_node 

            if(gui_callback_fn(ext_node)):
                break
            
            self.total_extends += 1

            for neighbor in ext_node.generate_neighbor_states():
                # You could filter at the enqueue step too, but it is not wholly necessary.
                if neighbor != ext_node.parent: # if neighbor not in ext_set: 
                    self.enqueue(neighbor, cutoff)
                    self.total_enqueues += 1
                    # It is tempting to add all enqueued states to the filter, but this
                    # can actually cause non-optimal results for Greedy and A*...

        return None 



"""
HELPFUL NOTES:

Python lists are fine to use as LIFO queues (aka stacks).
You might consider the append() and pop() methods.

However, python lists don't implement FIFO Queues very efficiently.
A "deque" (double-ended queue) improve on lists in this regard.
Consider the append(), appendleft(), pop(), and popleft() methods
https://docs.python.org/3/library/collections.html#collections.deque

A PriorityQueue implemention is provided for you - see priorityqueue.py.
It uses the heapq module to implement a heap.

When implementing a filter (aka graph search), it may be helpful to use the Set class.
Sets are like python dictionaries, except they only store keys.
The "in" keyword invokes a key lookup.
https://docs.python.org/3/tutorial/datastructures.html#sets
"""

#### Lab 1, Part 2b: Informed Search #################################################

class InformedSearchAgent(GoalSearchAgent):
    """
    Abstract class for Informed Goal Search Agents.
    The only change from GoalSearchAgent is a cost-heuristic is provided
    at __init__, and will be used during search.
    """
    heuristic : Callable[[StateNode],float]

    def __init__(self, heuristic : Callable[[StateNode],float], *args, **kwargs):
        """ To be overridden by subclasses (RandomWalk, RandomSearch, DFS, BFS, UCS, Greedy, and AStar)
        Create an empty frontier queue, 
        and initialize self.total_extends and self.total_enqueues to 0s. 
        Will be called by GUI before any search.
        """
        super().__init__(heuristic = heuristic, *args, **kwargs) # pass any unused parameters to any superclasses
        self.heuristic = heuristic
    

class GreedyBestSearch(InformedSearchAgent):
    """ Partial class representing a search strategy.
    Needs to be subclassed (multiple inheritance) with a mixin that
    that implements a search algorithm (i.e. TreeSearchAgent or GraphSearchAgent)

    Greedy Best is implemented with a priority queue. 
    """
    frontier : List[Tuple[float, StateNode]]

    def __init__(self, heuristic : Callable[[StateNode],float]):
        """ Create an empty frontier queue, 
        and initialize self.total_extends and self.total_enqueues to 0s. 
        Also takes the heuristic function to be used as an estimate
        of the remaining cost to goal. 
        """
        super().__init__(heuristic)
        self.frontier = []

        
    def enqueue(self, state: StateNode, cutoff: Union[int, float] = INF):
        """ Add the state to the frontier, unless path COST exceeds the cutoff """
        if state.path_cost < cutoff:
            heapq.heappush(self.frontier, (self.heuristic(state), state))

        
    def dequeue(self) -> Tuple[float, StateNode]:
        """  Choose and remove the state with LOWEST ESTIMATED REMAINING COST TO GOAL from the frontier."""
        return heapq.heappop(self.frontier)[1]


class AStarSearch(InformedSearchAgent):
    """ Partial class representing a search strategy.
    Needs to be subclassed (multiple inheritance) with a mixin that
    that implements a search algorithm (i.e. TreeSearchAgent or GraphSearchAgent)

    A* is implemented with a priority queue. 
    """
    frontier : List[Tuple[float, StateNode]]

    def __init__(self, heuristic : Callable[[StateNode],float], *args, **kwargs):
        """ Create an empty frontier queue, 
        and initialize self.total_extends and self.total_enqueues to 0s. 
        Also takes the heuristic function to be used as an estimate
        of remaining path cost. 
        """
        super().__init__(heuristic, *args, **kwargs)
        self.frontier = []

        
    def enqueue(self, state: StateNode, cutoff: Union[int, float] = INF):
        """ Add the state to the frontier, unless path COST exceeds the cutoff """
        if state.path_cost < cutoff:
            heapq.heappush(self.frontier, (state.path_cost + self.heuristic(state), state))

        
    def dequeue(self) -> StateNode:
        """  Choose, remove, and return the state with LOWEST ESTIMATED TOTAL PATH COST from the frontier."""
        return heapq.heappop(self.frontier)[1]


""" Informed search algorithms can be reconfigured to provide a "closest" answer
if . This often happens because of early termination (by max length/cost cutoff or time limit).

The change is simple: during search, keep track of the state/path that is closest to the goal, 
according to the cost heuristic, and return it if the search ultimately fails/terminates early.
 
This is sometimes known as an "anytime" algorithm, because the algorithm can have at least
*some* useful result anytime the agent needs one.
"""

class AnytimeSearchAlgorithmMixin(InformedSearchAgent):
    """
    Mixin class for "anytime" graph search algorithm.

    If terminating without finding the solution, returns the "best so far" solution with 
    the lowest estimated cost to goal, according to self.heuristic.
    
    Needs to be mixed in with a "strategy" subclass of GoalSearchAgent that
    implements the other methods (i.e. RandomSearch, DFS, BFS, UCS, etc.)
    """

    def search(self, 
            initial_state : StateNode, 
            gui_callback_fn : Callable[[StateNode],bool] = lambda : False,
            cutoff : Union[int, float] = INF 
            ) -> Optional[StateNode]:
        """ Perform an "Anytime" search from the initial_state
        
        """
        # Keep track of the closest path found yet
        anytime_result  : Tuple[StateNode, float] = (None, INF) 
        ext_filter : Set[StateNode] = set() 
        self.enqueue(initial_state)
        while self.frontier: 
            ext_node = self.dequeue()       

            if ext_node in ext_filter:
                continue

            ext_filter.add(ext_node)

            if ext_node.is_goal_state():
                return ext_node 
            
            # Check if new best anytime option
            dist = self.heuristic(ext_node)
            if dist < anytime_result[1]:
                anytime_result = (ext_node, dist)

            if(gui_callback_fn(ext_node)):
                break
            
            self.total_extends += 1

            for neighbor in ext_node.generate_neighbor_states():
                if neighbor != ext_node.parent: # if neighbor not in ext_set: 
                    self.enqueue(neighbor, cutoff)
                    self.total_enqueues += 1

        # Return the best path so far.
        return anytime_result[0]


### Part 3: Completely Optional Extensions ########################################################

""" If you're bored, try any of the following extensions!
"""


""" A) Investigate a way to determine if a given puzzle is solvable without exhausting the whole state space.
 You may want to research the concept of parity. Implement is_solvable and make sure that it returns True on all the
 solvable test boards while returning False on the unsolvable ones.
 """

# from slidepuzzle_problem import SlidePuzzleState
# def is_solvable(board : SlidePuzzleState):
#     """is this board solvable? return a boolean"""
#     raise NotImplementedError


""" B) A* is optimal, but its memory usage is still prohibitive for large state spaces.
Investiate and implement one of the following: Recursive Best-First Search (RBFS), memory-bounded A* (MA*)
or simplified memory-bounded A* (SMA*). Be sure to comment it well to demonstrate you understand it!
"""


""" C) Improve upon these implementations! The framework given to you here
was designed to facilitate learning, not necessarily efficiency. 
There are many ways these algorithms can be improved in terms of speed and memory usage.
Furthermore, and problem-specific agents can usually take advantage of 
specific properties for even more efficiency. 
"""

ALGORITHMS : Dict[str, Type[GoalSearchAgent] ] = {
    "tree": TreeSearchAlgorithmMixin, 
    "graph": GraphSearchAlgorithmMixin, 
    "anytime" : AnytimeSearchAlgorithmMixin
}

STRATEGIES : Dict[str, Type[GoalSearchAgent] ] = {
    "random": RandomSearch,
    "dfs": DepthFirstSearch,
    "bfs": BreadthFirstSearch,
    "ucs": UniformCostSearch,
    "greedy": GreedyBestSearch,
    "astar": AStarSearch,
}


ALL_AGENTS : Dict[str, Dict[str, Type[GoalSearchAgent] ]] = {}
for alg in ALGORITHMS:
    ALL_AGENTS[alg] = {}
    for strat in STRATEGIES:
        ALL_AGENTS[alg][strat] = type(alg + "-" + strat, (ALGORITHMS[alg], STRATEGIES[strat]), {})
