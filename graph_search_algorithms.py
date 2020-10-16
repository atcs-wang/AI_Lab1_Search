# Lab 1: 
# Name(s): Mr. Wang
# Email(s): matwan@bergen.org

from __future__ import annotations
from typing import List, Collection, Tuple, Callable, Optional, Union, Set, Dict, Type, Iterable
import random
from collections import deque
import heapq
from search_problem import StateNode, Action
from search_algorithms import GoalSearchAgent as gsa

PRINT_STUFF = True

INF = float('inf')

#### Lab 1, Part 1a: Uninformed Search #################################################

class GoalSearchAgent(gsa):
    """
    Abstract class for Goal Search Agents.
    """
    frontier : Collection[StateNode] # All Collections are "truthy" - they are True if not empty, False if empty
    total_extends : int 
    total_enqueues : int

    # ONLY FOR PRINTING LISTS
    enqueue_list = List
    extend_list = List


    """ __init__, enqueue, and dequeue be overridden by STRATEGY partial subclasses (i.e. RandomSearch, DFS, BFS, UCS, Greedy, and AStar)"""

    def __init__(self, *args, **kwargs):
        """Initialize self.total_extends and self.total_enqueues to 0s. 
        Subclasses should initialize an empty frontier that enqueue() and dequeue() operate on.
        """
        super().__init__()
        self.total_extends = 0
        self.total_enqueues = 0
        self.enqueue_list = []
        self.extend_list = []

    def enqueue(self, state: StateNode, cutoff: Union[int, float] = INF):
        """ Add the state to the frontier, unless some property (e.g. depth/path cost) exceeds the cutoff """
        # Subclasses will override and implement.
        raise NotImplementedError
        
    def dequeue(self) -> StateNode:
        """ Choose, remove, and return a state from the frontier """
        # Subclasses will override and implement.
        raise NotImplementedError

    """ search to be implemented by ALGORITHM partial subclasses (i.e. TreeSearch, GraphSearch, AnytimeSearch)"""

    def search(self, 
            initial_state : StateNode, 
            gui_callback_fn : Callable[[StateNode],bool] = lambda : False,
            cutoff : Union[int, float] = INF 
            ) -> Optional[StateNode]:
        """ To be overridden by algorithm subclasses (TreeSearchAgent, GraphSearchAgent, AnytimeSearchAlgorithm)
        Returns a StateNode representing a solution path to the goal state, or None if search failed.
        """
        raise NotImplementedError

    def print_lists(self):
        print("Extended: " + self.get_extend_list())
        print("Enqueued: " +  self.get_enqueue_list())

    def get_extend_list(self):
        return ", ".join(self.extend_list)

    def get_enqueue_list(self):
        return ", ".join(self.enqueue_list).replace("[, ", "[").replace(", ]", "]").replace("[", "\n[")

class RandomSearch(GoalSearchAgent):
    """ Partial class representing the Random Search strategy.
    To be subclassed (multiple inheritance) with a mixin that
    that implements search (i.e. TreeSearchAgent or GraphSearchAgent)
    """
    frontier : List[StateNode]
    
    def __init__(self, *args, **kwargs):
        """ Initialize self.total_extends and self.total_enqueues (done in super().__init__())
        Create an empty frontier queue.
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


# Optional helper function:
def generate_neighbor_states(statenode : StateNode) -> Iterable[StateNode]:
    """ Generate and return all possible neighbor states (all states that can result from taking legal actions in this state).
    The generated StateNode objects should have this StateNode as its parent, and action as its last_action.

    This method is a good candidate for using "yield" and writing a generator function instead of returning a list.
    """
    for action in statenode.get_all_actions():
        yield statenode.get_next_state(action)
    ### The above generator definition is equivalent to:
    # return (self.get_next_state(action) for a in self.get_all_actions())
    ### If it is better to get a List for the reusability, methods, or indexing:
    # return [self.get_next_state(action) for a in self.get_all_actions()]


class TreeSearchAlgorithm(GoalSearchAgent):
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
        """ Perform a search from the initial_state. Here is the pseudocode:
        
        - Enqueue the initial_state in the frontier
        - Repeat while there are still StateNodes in the frontier:
            1) Dequeue a StateNode
            2) If the StateNode is a goal state, return it (end the search)
            3) Extend the dequeued state by enqueueing all its neighboring states. 
                - Implement the "no backtracking" optimization: do not enqueue parent states 
                - Pass the cutoff parameter to enqueue. 
                - Update self.total_extends and self.total_enqueues appropriately
            4*) Call gui_callback_fn, passing it the extended StateNode. If it returns True, 
                end the search (the user has terminated early)
            
        - If the search ends because the frontier is empty or gui_callback_fn ended the search
        early, return None.

        Remember that "tree search" may re-enqueue or re-extend the same state, multiple times.
        """

        #TODO implement!
        self.enqueue(initial_state)
        if PRINT_STUFF:
            self.enqueue_list.append(str(initial_state))
        while self.frontier: #while frontier is not empty (returns False when empty)
            ext_node = self.dequeue()       # pop from queue and extend

            if ext_node.is_goal_state():
                self.print_lists()
                return ext_node 

            if PRINT_STUFF:
                self.enqueue_list.append("[")
            for neighbor in generate_neighbor_states(ext_node):
                if neighbor != ext_node.parent: # This is the no-backtracking check
                    self.enqueue(neighbor, cutoff)
                    if PRINT_STUFF:
                        self.enqueue_list.append(str(neighbor))

                    self.total_enqueues += 1
            self.total_extends += 1
            if PRINT_STUFF:
                self.enqueue_list.append("]")
                self.extend_list.append(str(ext_node))

            if(gui_callback_fn(ext_node)):
                break


        self.print_lists()
            
        return None # if frontier ever empties without finding the goal, search has failed


class DepthFirstSearch(GoalSearchAgent):
    """ Partial class representing the Depth First Search strategy.
    To be subclassed (multiple inheritance) with a mixin that
    that implements search (i.e. TreeSearchAgent or GraphSearchAgent)

    DFS is implemented with a LIFO queue. A list is an efficient one. 
    """
    frontier : List[StateNode]
    
    def __init__(self, *args, **kwargs):
        """ Initialize self.total_extends and self.total_enqueues (done in super().__init__())
        Create an empty frontier queue.
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
    To be subclassed (multiple inheritance) with a mixin that
    that implements a search algorithm (i.e. TreeSearchAgent or GraphSearchAgent)

    BFS is implemented with a FIFO queue. 
    Lists are bad FIFO queues, but the deque data structure is an efficient implementation. 
    Check out the documentation of deque: https://docs.python.org/3/library/collections.html#collections.deque
    """
    frontier : deque[StateNode]
    
    def __init__(self, *args, **kwargs):
        """ Initialize self.total_extends and self.total_enqueues (done in super().__init__())
        Create an empty frontier queue.
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
    To be subclassed (multiple inheritance) with a mixin that
    that implements a search algorithm (i.e. TreeSearchAgent or GraphSearchAgent)

    UCS is implemented with a priority queue, which is typically a heap data structure. 
    The heapq library allows you to use a list as a efficient heap.
    (heapq.heappush and heapq.heappop are the main methods).
    Since states aren't ordered, the elements of the list-heap should be 
    tuples of (priority_value, statenode). heapq orders elements by the first element.

    Check out the documentation of heapq: https://docs.python.org/3/library/heapq.html
    """
    frontier : List[Tuple[float, StateNode]]
    
    def __init__(self,*args, **kwargs):
        """ Initialize self.total_extends and self.total_enqueues (done in super().__init__())
        Create an empty frontier queue.
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

class GraphSearchAlgorithm(GoalSearchAgent):
    """
    Mixin class for the graph search (extended state filter) algorithm.
    
    Needs to be mixed in with a "strategy" subclass of GoalSearchAgent that
    implements the other methods (i.e. RandomSearch, DFS, BFS, UCS, etc.)

    When implementing a efficient filter, you'll want to use sets, not lists.
    Sets are like python dictionaries, except they only store keys (no values).
    The "in" keyword invokes a key lookup.
    Check out the documentation: https://docs.python.org/3/tutorial/datastructures.html#sets
    """
    def search(self, 
            initial_state : StateNode, 
            gui_callback_fn : Callable[[StateNode],bool] = lambda : False,
            cutoff : Union[int, float] = INF 
            ) -> Optional[StateNode]:
        """ Perform a search from the initial_state, which constitutes the initial frontier.
        
        Graph search is similar to tree search, but it manages an "extended filter" 
        to avoid re-extending previously extended states again.

        Create a set of extended states. Before extending any state, check if the state has already been extended.
        If so, skip it. Otherwise, extend and add to the set. 
        """
        ext_filter : Set[StateNode] = set() # Create an empty extended state filter

        #TODO implement! (You may start by copying your TreeSearch's code)
        self.enqueue(initial_state)
        if PRINT_STUFF:
            self.enqueue_list.append(str(initial_state))

        while self.frontier: 
            ext_node = self.dequeue()       

            # When dequeueing, check if previously extended.
            if ext_node in ext_filter:
                continue

            # Add the (about to be) extended state to the filter
            ext_filter.add(ext_node)

            if ext_node.is_goal_state():
                self.print_lists()
                return ext_node 

            if PRINT_STUFF:
                self.enqueue_list.append("[")

            for neighbor in generate_neighbor_states(ext_node):
                # You could filter at the enqueue step too, but it is not wholly necessary.
                if neighbor != ext_node.parent: # if neighbor not in ext_set: 
                    self.enqueue(neighbor, cutoff)
                    self.total_enqueues += 1
                    if PRINT_STUFF:
                        self.enqueue_list.append(str(neighbor))
                    # It is tempting to add all enqueued states to the filter, but this
                    # can actually cause non-optimal results for Greedy and A*...
            self.total_extends += 1
            if PRINT_STUFF:
                self.enqueue_list.append("]")
                self.extend_list.append(str(ext_node))
            if(gui_callback_fn(ext_node)):
                break
            
            
        self.print_lists()
        return None 



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
    To be subclassed (multiple inheritance) with a mixin that
    that implements a search algorithm (i.e. TreeSearchAgent or GraphSearchAgent)

    Greedy Best is implemented with a priority queue. 
    """
    frontier : List[Tuple[float, StateNode]]

    def __init__(self, heuristic : Callable[[StateNode],float]):
        """ Initialize self.total_extends and self.total_enqueues(done in super().__init__())
        Create an empty frontier queue.
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
    To be subclassed (multiple inheritance) with a mixin that
    that implements a search algorithm (i.e. TreeSearchAgent or GraphSearchAgent)

    A* is implemented with a priority queue. 
    """
    frontier : List[Tuple[float, StateNode]]

    def __init__(self, heuristic : Callable[[StateNode],float], *args, **kwargs):
        """ Initialize self.total_extends and self.total_enqueues (done in super().__init__())
        Create an empty frontier queue.
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

class AnytimeSearchAlgorithm(InformedSearchAgent):
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

        This is the same as a graph search, but even if the search fails to find a solution, 
        it should always return the lowest-cost StateNode path  to the state closest* to the solution found so far.
        *Closest according to the agent's heuristic.
        """
        # Keep track of the closest path found yet
        anytime_result  : Tuple[StateNode, float, float] = (None, INF, INF) 
        ext_filter : Set[StateNode] = set() 
        self.enqueue(initial_state)
        if PRINT_STUFF:
            self.enqueue_list.append(str(initial_state))
        while self.frontier: 
            ext_node = self.dequeue()       

            if ext_node in ext_filter:
                continue

            ext_filter.add(ext_node)

            if ext_node.is_goal_state():
                self.print_lists()
                return ext_node 
            
            # Check if new best anytime option
            dist = self.heuristic(ext_node)
            if dist < anytime_result[1] or (dist == anytime_result[1] and ext_node.path_cost < anytime_result[2]):
                anytime_result = (ext_node, dist, ext_node.path_cost)            

            if PRINT_STUFF:
                self.enqueue_list.append("[")

            for neighbor in generate_neighbor_states(ext_node):
                if neighbor != ext_node.parent: # if neighbor not in ext_set: 
                    self.enqueue(neighbor, cutoff)
                    self.total_enqueues += 1
                    if PRINT_STUFF:
                        self.enqueue_list.append(str(neighbor))

            self.total_extends += 1
            if PRINT_STUFF:
                self.enqueue_list.append("]")
                self.extend_list.append(str(ext_node))

            if(gui_callback_fn(ext_node)):
                break
        self.print_lists()
        # Return the best path so far.
        return anytime_result[0]


# Extra stuff added:
EXTRA_STUFF = True

class DepthFirstSearch_PQ(GoalSearchAgent):
    """ DFS implemented with a Priority Queue. 
    This implementation will tie-break based on natural ordering of states, as defined in the 
    __lt__() function.
    """   
    frontier : List[Tuple[float, StateNode]]
    
    def __init__(self,*args, **kwargs):
        """ Initialize self.total_extends and self.total_enqueues (done in super().__init__())
        Create an empty frontier queue.
        """
        super().__init__(*args, **kwargs)
        self.frontier = []

        
    def enqueue(self, state: StateNode, cutoff: Union[int, float] = INF):
        """ Add the state to the frontier, unless path COST exceeds the cutoff 
        The priority is negatve depth, so the deepest node has priority.
        """
        if state.depth < cutoff:
            heapq.heappush(self.frontier, (-state.depth, state))

        
    def dequeue(self) -> StateNode:
        """  Choose, remove, and return the state with  so the DEEPEST node is dequeued from the frontier."""
        return heapq.heappop(self.frontier)[1]

class BreadthFirstSearch_PQ(GoalSearchAgent):
    """ BFS implemented with a Priority Queue. 
    This implementation will tie-break based on natural ordering of states, as defined in the 
    __lt__() function.
    """   
    frontier : List[Tuple[float, StateNode]]
    
    def __init__(self,*args, **kwargs):
        """ Initialize self.total_extends and self.total_enqueues (done in super().__init__())
        Create an empty frontier queue.
        """
        super().__init__(*args, **kwargs)
        self.frontier = []

        
    def enqueue(self, state: StateNode, cutoff: Union[int, float] = INF):
        """ Add the state to the frontier, unless path COST exceeds the cutoff 
        The priority is depth, so the shallowest node has priority.
        """
        if state.depth < cutoff:
            heapq.heappush(self.frontier, (state.depth, state))

        
    def dequeue(self) -> StateNode:
        """  Choose, remove, and return the state with  so the SHALLOWEST node is dequeued from the frontier."""
        return heapq.heappop(self.frontier)[1]



class TreeSearchNoTailBiteAlgorithm(GoalSearchAgent):
    """
    Mixin class for the tree search algorithm (without tail-biting).

    Needs to be mixed in with a "strategy" subclass of GoalSearchAgent that
    implements the other methods (i.e. RandomSearch, DFS, BFS, UCS, etc.)
    """
    def search(self, 
            initial_state : StateNode, 
            gui_callback_fn : Callable[[StateNode],bool] = lambda : False,
            cutoff : Union[int, float] = INF 
            ) -> Optional[StateNode]:
        """ Perform a search from the initial_state. Here is the pseudocode:
        
        - Enqueue the initial_state in the frontier
        - Repeat while there are still StateNodes in the frontier:
            1) Dequeue a StateNode
            2) If the StateNode is a goal state, return it (end the search)
            3*) Call gui_callback_fn, passing it the dequeued StateNode. If it returns True, 
                end the search (the user has terminated early)
            4) Extend the dequeued state by enqueueing all its neighboring states. 
                - Implement the "no TAIL BITE" optimization: do not enqueue parent states 
                - Pass the cutoff parameter to enqueue. 
                - Update self.total_extends and self.total_enqueues appropriately
        - If the search ends because the frontier is empty or gui_callback_fn ended the search
        early, return None.

        Remember that "tree search" may re-enqueue or re-extend the same state, multiple times.
        """
        self.enqueue(initial_state)
        if PRINT_STUFF:
            self.enqueue_list.append(str(initial_state))

        while self.frontier: #while frontier is not empty (returns False when empty)
            ext_node = self.dequeue()       # pop from queue and extend

            if ext_node.is_goal_state():
                self.print_lists()
                return ext_node 


            if PRINT_STUFF:
                self.enqueue_list.append("[")

            for neighbor in generate_neighbor_states(ext_node):
                if neighbor not in ext_node.get_path(): # This is the no-tail-bite check. Its very not efficient.
                    self.enqueue(neighbor, cutoff)
                    self.total_enqueues += 1
                    if PRINT_STUFF:
                        self.enqueue_list.append(str(neighbor))
            self.total_extends += 1
            if PRINT_STUFF:
                self.enqueue_list.append("]")
                self.extend_list.append(str(ext_node))

            if(gui_callback_fn(ext_node)):
                break
        self.print_lists()
        return None # if frontier ever empties without finding the goal, search has failed



# Collection of all the above 

ALGORITHMS : Dict[str, Type[GoalSearchAgent] ] = {
    "tree": TreeSearchAlgorithm, 
    "graph": GraphSearchAlgorithm, 
    "anytime" : AnytimeSearchAlgorithm,
}

if EXTRA_STUFF:
    ALGORITHMS["tree-no-tail-bite"] = TreeSearchNoTailBiteAlgorithm


STRATEGIES : Dict[str, Type[GoalSearchAgent] ] = {
    "random": RandomSearch,
    "dfs": DepthFirstSearch,
    "bfs": BreadthFirstSearch,
    "ucs": UniformCostSearch,
    "greedy": GreedyBestSearch,
    "astar": AStarSearch,
}

if EXTRA_STUFF:
    STRATEGIES["dfs-pq"] = DepthFirstSearch_PQ
    STRATEGIES["bfs-pq"] = BreadthFirstSearch_PQ


"""
Dynamically generate all class types that result from mixing the ALGORITHMS with the STRATEGIES
"""
ALL_AGENTS : Dict[str, Dict[str, Type[GoalSearchAgent] ]] = {}
for alg in ALGORITHMS:
    ALL_AGENTS[alg] = {}
    for strat in STRATEGIES:
        ALL_AGENTS[alg][strat] = type(alg + "-" + strat, (ALGORITHMS[alg], STRATEGIES[strat]), {})


### Completely Optional Extensions ########################################################

""" If you're bored, try any of the following extensions!
"""


""" A) Investigate a way to determine if a given slide puzzle is solvable without exhausting the whole state space.
 You may want to research the concept of parity. Implement is_solvable and make sure that it returns True on all the
 solvable test boards while returning False on the unsolvable ones.
 Write a script to open and test different slide puzzle boards.
 """

# from slidepuzzle_problem import SlidePuzzleState
# def is_solvable(board : SlidePuzzleState):
#     """is this board solvable? return a boolean"""
#     raise NotImplementedError


""" B) A* is optimal, but its memory usage is still prohibitive for large state spaces.
Investiate and implement one or more of the following: Recursive Best-First Search (RBFS), memory-bounded A* (MA*)
or simplified memory-bounded A* (SMA*).
"""


""" C) Improve upon these implementations! The framework given to you here
was designed to facilitate learning, not necessarily efficiency. 
There are many ways these algorithms can be improved in terms of speed and memory usage.
Furthermore, and problem-specific agents can usually take advantage of 
specific properties for even more efficiency. 
"""