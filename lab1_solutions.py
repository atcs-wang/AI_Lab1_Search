# Lab 1: 8-puzzle. (Based on a COS226 assignment from Princeton University)
# Name(s): Mr. Wang
# Email(s): matwan@bergen.org
import random
from collections import deque
from priorityqueue import PriorityQueue
from statenode import StateNode

INF = float('inf')

#### Lab 1, Part 1a: Uninformed Search #################################################

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


def RandWalk(initial_state, avoid_backtrack = False, filtering = False, cutoff = INF,
        state_callback_fn = lambda state : False, # A callback function. If it returns True, terminate
        counter = {'num_enqueues':0, 'num_extends':0}):

    frontier = [initial_state]
    extended_list = set()
    while frontier: # frontier is False when it is empty. So just keep going until out of places to go...

        # choose from frontier
        ext_node = random.choice(frontier)

        ### filtering -added
        if filtering:
            extended_list.add(ext_node)
        ###

        counter['num_extends'] += 1
        if ext_node.is_goal_state():
            return ext_node
        if(state_callback_fn(ext_node)):
            break

        ### max depth cutoff - added
        if ext_node.get_path_length() >= cutoff:
            break
        ###

        ### Update frontier
        frontier = ext_node.generate_next_states()
        # If avoid_backtrack, don't add parent state
        if avoid_backtrack:
            frontier = [x for x in frontier if not (ext_node.get_parent() == x)]

        counter['num_enqueues'] += len(frontier)
        ### filtering - added
        if filtering:    # skip if previously extended
            filtered_states = []
            for node in frontier:
                if node in extended_list:
                    continue
                filtered_states.append(node)
            frontier = filtered_states
        ###

    return None
    # if loop breaks before finding goal, search is failure



def GenericSearch (initial_state, frontier,
        dequeue_fn, # lambda frontier : None,
        enqueue_fn, # lambda frontier, state : None,
        avoid_backtrack = False, filtering = False, cutoff = INF,
        state_callback_fn = lambda state : False, # A callback function for extended states. If it returns True, terminate
        counter = {'num_enqueues':0, 'num_extends':0}): # A counter for tracking stats

    enqueue_fn(frontier, initial_state)
    extended_list = set()
    while frontier: #while frontier is not empty (returns False when empty)
        ext_node = dequeue_fn(frontier)       # pop from queue and extend

        # max cost cutoff
        if ext_node.get_path_length() > cutoff:
            continue


        if filtering:    # skip if previously extended
            if ext_node in extended_list:
                continue
            extended_list.add(ext_node)
        counter['num_extends'] += 1

        if(state_callback_fn(ext_node)):
            break

        if ext_node.is_goal_state():
            return ext_node # SolutionPath(final_state = ext_node, num_enqueues = num_enqueues, num_extends = num_extends)


        for neighbor in ext_node.generate_next_states():
            if avoid_backtrack and neighbor == ext_node.get_parent():
                continue
            # enqueue children in frontier
            enqueue_fn(frontier, neighbor)
            counter['num_enqueues'] += 1

    return None # SolutionPath(final_state = None, num_enqueues = num_enqueues, num_extends = num_extends)
    # if frontier ever empties without finding the goal, search has failed


def DFS(initial_state, avoid_backtrack = False, filtering = False, cutoff = INF,
        state_callback_fn = lambda state : False, # A callback function. If it returns True, terminate
        counter = {'num_enqueues':0, 'num_extends':0}):


    def dequeue(frontier):
        return frontier.pop()

    def enqueue(frontier, state):
        frontier.append(state)

    return GenericSearch(initial_state, frontier = deque(),
        dequeue_fn = dequeue,
        enqueue_fn = enqueue,
        avoid_backtrack = avoid_backtrack, filtering = filtering, cutoff = cutoff,
        state_callback_fn = state_callback_fn,
        counter = counter
        )

def BFS(initial_state, avoid_backtrack = False, filtering = False, cutoff = INF,
        state_callback_fn = lambda state : False, # A callback function. If it returns True, terminate
        counter = {'num_enqueues':0, 'num_extends':0}):

    def dequeue(frontier):
        return frontier.popleft()

    def enqueue(frontier, state):
        frontier.append(state)

    return GenericSearch(initial_state, frontier = deque(),
        dequeue_fn = dequeue,
        enqueue_fn = enqueue,
        avoid_backtrack = avoid_backtrack, filtering = filtering, cutoff = cutoff,
        state_callback_fn = state_callback_fn,
        counter = counter
        )



#Perform Uniform Cost Search
def UCS(initial_state, avoid_backtrack = False, filtering = False, cutoff = INF,
        state_callback_fn = lambda state : False, # A callback function for extended states. If it returns True, terminate
        counter = {'num_enqueues':0, 'num_extends':0}): # A counter for

    def dequeue(frontier):
        return frontier.pop()

    def enqueue(frontier, state):
        frontier.append(state, state.get_path_cost())

    return GenericSearch(initial_state, frontier = PriorityQueue(),
        dequeue_fn = dequeue,
        enqueue_fn = enqueue,
        avoid_backtrack = avoid_backtrack, filtering = filtering, cutoff = cutoff,
        state_callback_fn = state_callback_fn,
        counter = counter
        )


#### Lab 1, Part 2b: Informed Search #################################################


#Perform Greedy Best Search
def GreedyBest(initial_state, heuristic_fn,
        avoid_backtrack = False, filtering = False, cutoff = INF,
        state_callback_fn = lambda state : False, # A callback function for extended states. If it returns True, terminate
        counter = {'num_enqueues':0, 'num_extends':0}): # A counter for

    def dequeue(frontier):
        return frontier.pop()

    def enqueue(frontier, state):
        frontier.append(state, heuristic_fn(state))

    return GenericSearch(initial_state, frontier = PriorityQueue(),
        dequeue_fn = dequeue,
        enqueue_fn = enqueue,
        avoid_backtrack = avoid_backtrack, filtering = filtering, cutoff = cutoff,
        state_callback_fn = state_callback_fn,
        counter = counter
        )


    return None # SolutionPath(final_state = None, num_enqueues = num_enqueues, num_extends = num_extends)
    # if frontier ever empties without finding the goal, search has failed


def AStar(initial_state, heuristic_fn,
        avoid_backtrack = False, filtering = False, cutoff = INF,
        state_callback_fn = lambda state : False, # A callback function for extended states. If it returns True, terminate
        counter = {'num_enqueues':0, 'num_extends':0}): # A counter for

    def dequeue(frontier):
        return frontier.pop()

    def enqueue(frontier, state):
        frontier.append(state, state.get_path_cost() + heuristic_fn(state))

    return GenericSearch(initial_state, frontier = PriorityQueue(),
        dequeue_fn = dequeue,
        enqueue_fn = enqueue,
        avoid_backtrack = avoid_backtrack, filtering = filtering, cutoff = cutoff,
        state_callback_fn = state_callback_fn,
        counter = counter
        )




### Part 3: Completely Optional Extensions ########################################################

""" If you're bored, try any of the following extensions!
"""


""" A) Investigate a way to determine if a given puzzle is solvable without exhausting the whole state space.
 You may want to research the concept of parity. Implement is_solvable and make sure that it returns True on all the
 solvable test boards while returning False on the unsolvable ones.
 """

def is_solvable(board) :
    """is this board solvable? return a boolean"""
    raise NotImplementedError


""" B)
Greedy-Best is an informed analogue to BFS.
Hill-Climbing is an informed analogue to DFS.

"""
"""
The sort() method of lists may come in handy here. If you sort a list of tuples,
it will sort by the value of the first element.
"""

def HillClimbingDFS(initial_state, heuristic_fn, avoid_backtrack = False, filtering = False, cutoff = INF, visualize_fn = lambda *args: None):



    frontier = deque()
    frontier.append(initial_state)
    extended_list = set()
    while frontier: #while frontier is not empty (returns False when empty)
        ext_node = frontier.pop()         # pop from queue and extend

        if filtering:    # skip if previously extended
            if ext_node in extended_list:
                continue
            extended_list.add(ext_node)
        num_extends += 1

        visualize_fn(ext_node)
        if ext_node.is_goal_state():
            return SolutionPath(final_state = ext_node, num_enqueues = num_enqueues, num_extends = num_extends)

        # max depth cutoff
        if ext_node.get_path_length() >= cutoff:
            continue

        ordered_nbrs = ext_node.generate_next_states()
        ordered_nbrs.sort(key = heuristic_fn, reverse = True)
        # we want to put the lowest values last so they to get pushed on TOP of the frontier stack

        for neighbor in ordered_nbrs:
            if avoid_backtrack and neighbor == ext_node.get_parent():
                continue

            # enqueue in frontier
            frontier.append(neighbor)
            num_enqueues += 1

    return SolutionPath(final_state = None, num_enqueues = num_enqueues, num_extends = num_extends)
    # if frontier ever empties without finding the goal, search has failed



""" C) Informed search algorithms can be used as "anytime" algorithms because,
if terminated early, they can provide a path to the state closest to the goal that its
seen so far - which, when on a time crunch, is much better than nothing!
Add the function get_closest_path to Hill-Climbing (and others??) so that,
if it does not find the solution in the max depth limit, it returns a path
to the node with the lowest heuristic value it has seen yet.
"""
    # def get_closest_path(self) :
    #     """ If solution is found, returns the solution. Otherwise, returns a path to the
    #     node with the lowest heuristic value found. """
    #     raise NotImplementedError



""" D) Implement a better admissible/consistent heuristic function for A* than hamming or manhattan. There is some literature
on this, but an original one would be extra impressive! Test A* with it to see if it finds an optimal solution
faster than manhattan!
"""

def better_heuristic(board) :
    raise NotImplementedError


""" E) A* is optimal, but its memory usage is still prohibitive for large state spaces.
Investiate and Implement either Recursive Best-First Search (RBFS), memory-bounded A* (MA*)
or simplified memory-bounded A* (SMA*). Be sure to comment it well to demonstrate you understand it!
"""
