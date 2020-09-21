
from __future__ import annotations
from typing import Optional, Any, Hashable, Sequence, Iterable, Dict, Union, List, Tuple

from search_problem import StateNode, Action
from collections import OrderedDict

### A generic graph traversal problem. 

class GraphAction(Action):
    def __init__(self, state : str):
        self.state = str(state)

    def __str__(self) -> str:
        """ Returns a string that describes this action """
        return self.state

    def __eq__(self, o) -> bool:
        return o.state == self.state

class GraphState(StateNode):
    """ A state node for the graph environment. """

    """ Type Hints allow for the optional type declaration of "instance variables" this way, like Java.
        It is recommended you list them here:
    """
    # The graph maps states to neighbor states, which map to their transition cost.
    # If the Dict maps to None, then it is a goal state.
    graph : OrderedDict[str, Union[None,OrderedDict[str, float]]]
    heuristics : Dict[str, float]
    this_state : str
    
    @staticmethod
    def readFromFile(filename : str) -> StateNode:
        """Reads data from a text file and returns a GraphState which is an initial state."""
        with open(filename, 'r') as file:
            #number of states
            n = int(file.readline())
            graph = OrderedDict()
            heuristics = {}
            for i in range(n):
                str_state_heuristic, str_transitions = file.readline().split(":")
                state, heuristic = str_state_heuristic.split("?") 
                state = state.strip()
                heuristics[state] = float(heuristic)

                if str_transitions.strip().lower() == "goal":
                    transitions = None
                else:
                    transitions = OrderedDict()
                    for str_state_cost in str_transitions.split(";"):
                        to_state, cost = str_state_cost.split(",")
                        transitions[to_state.strip()] = float(cost)
                graph[state] = transitions
            init = file.readline()
            return GraphState(graph = graph,
                            heuristics = heuristics,
                            this_state = init,
                            parent = None,
                            last_action = None,
                            depth = 0,
                            path_cost = 0.0)

    #Override
    def __init__(self, 
            graph :  Dict[str, Union[None,Dict[str, float]]],
            heuristics : Dict[str, float],
            this_state : str,
            parent : Optional[StateNode], 
            last_action: Optional[GraphAction], 
            depth : int, 
            path_cost : float = 0.0) :
        """Creates a GraphState that represents a state of the environment and context for how the agent gets 
        to this state (the path, aka a series of state-action transitions).
        
        Keyword Arguments:
        All the arguments for StateNode's __init__; Use super.__init__() to call this function and pass appropriate parameters.
        tiles -- a tuple grid of integers representing the position of different numbered tiles
        empty_pos -- a coordinate indicating the position of the empty spot (tile 0)
        """
        super().__init__(parent = parent, last_action = last_action, depth = depth, path_cost = path_cost)
        self.graph = graph
        self.heuristics = heuristics
        self.this_state = this_state

    """ Additional accessor methods - needed for the GUI"""

    def get_size(self) -> int:
        return len(self.graph)

    """ Overridden methods from StateNode """

    # Override
    def get_state_features(self) -> Hashable:
        """Returns a full featured representation of the state.
        
        If two GraphState objects represent the same state, get_features() should return the same for both objects.
        However, two GraphState with identical state features may not represent the same node of the search tree -
        that is, they may have different parents, last actions, path lengths/costs etc...
        """
        return self.this_state

    # Override
    def __str__(self) -> str:
        """Return a string representation of the state.
           
           This should return N lines of N numbers each, separated by whitespace,
           similar to the file format for initial states
        """
        return self.this_state
    
    # Override
    def is_goal_state(self) -> bool:
        """Returns if a goal (terminal) state. 
        The goal of the slide puzzle is to have the empty spot in the 0th row and col,
        and then the rest of the numbered tiles in row-major order!
        """
        return self.graph[self.this_state] is None

    # Override
    def is_legal_action(self, action : GraphAction) -> bool:
        """Returns whether an action is legal from the current state

        Actions in the slide puzzle environment involve moving a tile into
        the adjacent empty spot.
        It is up to the coder to define a datatype for representing actions,
        and also then what constitutes a legal action in a state.
        
        One possible way to represent action is as the GraphAction of the tile that
        is to be moved into the empty slot. It needs to be not out of bounds, and 
        actually adjacent.
        """
        if self.is_goal_state():
            return False
        return action.state in self.graph[self.this_state]

    # Override
    def get_all_actions(self) -> Iterable[GraphAction]:
        """Return all legal actions at this state."""
        if self.is_goal_state():
            return
        for s in self.graph[self.this_state]:
            yield GraphAction(s)

    # Override
    def describe_last_action(self) -> str:
        """Returns a string describing the last_action taken (that resulted in transitioning from parent to this state)
        (Can be None or "None" if the initial state)

        The action should be described as "Moved tile X" where X is the tile number
        that last got slid into the empty spot.
        """
        if self.last_action is None:
             return None 
        return self.parent.this_state + " -> " + self.this_state

    # Override
    def get_next_state(self, action : GraphAction) -> GraphState:
        """ Return a new StateNode that represents the state that results from taking the given action from this state.
        The new StateNode object should have this StateNode (self) as its parent, and action as its last_action.

        -- action is assumed legal (is_legal_action called before), but a ValueError may be passed for illegal actions if desired.
        """
        return GraphState(graph = self.graph,
                        heuristics = self.heuristics,
                        this_state = action.state,
                        parent = self,
                        last_action = action,
                        depth = self.depth + 1,
                        path_cost = self.path_cost + self.graph[self.this_state][action.state],
                        )
