from __future__ import annotations
from typing import Optional, Any, Hashable, Sequence, Iterable
"""
An abstract state node for a goal-based search problem.

This is not meant to be used directly
as an object, but serves as a abstract parent object for various
state-search-problem representations.

Your search algorithms will use StateNode objects, making them generalizable
for all kinds of problems.
"""
class StateNode:

    """ Type Hints allow for the optional type declaration of "instance variables" this way, like Java """
    parent : StateNode
    last_action : Any
    path_length : int
    path_cost : float


    @staticmethod
    def readFromFile(filename : str) -> StateNode:
        """Reads data from a text file and returns a StateNode which is an initial state.
        This should be implemented in subclasses to read problem specific, user-designed file formats. 
        """
        raise NotImplementedError

    
    def __init__(self, 
                parent : Optional[StateNode], 
                last_action: Optional[Any], 
                path_length : int, 
                path_cost : float = 0.0) :
        """Creates a StateNode that represents a state of the environment and context for how the agent gets 
        to this state (the path, aka a series of state-action transitions).
        
        Keyword Arguments:
        parent -- the preceding StateNode along the path to reach this state. None, for an initial state.
        last_action -- the preceding action taken along the path to reach this state. None, for an initial state. 
        path_length -- the number of state-action transitions taken in the path to reach this state.
        path_cost -- the accumulated cost of the entire path to reach this state

        In any subclass of StateNode, the __init__() should take additional parameters that help define its state features.
        Use super.__init__() to call this function and pass appropriate parameters.
        """
        self.parent = parent
        self.last_action = last_action
        self.path_length = path_length
        self.path_cost = path_cost


    def get_all_features(self) -> Hashable:
        """Returns a full featured representation of the state.

        This should return something consistent, immutable, and hashable - primitives, strings, and tuples of such (generally no lists or objects).

        If two StateNode objects represent the same state, get_features() should return the same for both objects.
        Note, however, that two states with identical features may have been arrived at from different paths.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """Return a string representation of the state."""
        raise NotImplementedError

    def is_goal_state(self) -> bool:
        """Returns if a goal (terminal) state."""
        raise NotImplementedError

    def is_legal_action(self, action : Any) -> bool:
        """Returns whether an action is legal from the current state"""
        raise NotImplementedError

    def get_all_actions(self) -> Iterable[Any]:
        """Return all legal actions from this state. Actions may be whatever type you wish."""
        raise NotImplementedError

    def describe_last_action(self) -> str:
        """Returns a string describing the last_action taken (that resulted in transitioning from parent to this state)
        (Can be None or "None" if the initial state)
        It is not necessary to override, but may be nice for readability.
        """
        return str(self.last_action)


    def get_next_state(self, action : Any) -> StateNode:
        """ Return a new StateNode that represents the state that results from taking the given action from this state.
        The new StateNode object should have this StateNode (self) as its parent, and action as its last_action.

        -- action is assumed legal (is_legal_action called before), but a ValueError may be passed for illegal actions if desired.
        """
        raise NotImplementedError

    ## TODO Should these be left as an exercise for students? Or moved to the algorithms?

    def generate_neighbor_states(self) -> Iterable[StateNode]:
        """ Generate and return all possible neighbor states (all states that can result from taking legal actions in this state).
        The generated StateNode objects should have this StateNode as its parent, and action as its last_action.

        This method is a good candidate for using "yield" and writing a generator function instead of returning a list.
        """
        for a in self.get_all_actions():
            yield self.get_next_state(action)
        ### The above generator definition is equivalent to:
        # return (self.get_next_state(action) for a in self.get_all_actions())
        ### If it is better to get a List for the reusability, methods, or indexing:
        # return [self.get_next_state(action) for a in self.get_all_actions()]

    
    def get_path(self) -> Sequence[StateNode]:
        """Returns a sequence (list) of StateNodes representing the path from the initial state to this state.

        You do not need to override this method.
        """
        path = [self]
        s = self.get_parent()
        while s is not None :
            path.append(s)
            s = s.get_parent()
        path.reverse()
        return path

    
    def __lt__(self, other) -> bool:
        """
        Leave this function alone; it is needed to make tuple comparison work with heapq (PriorityQueue). 
        It doesn't actually describe any ordering.
        """
        return True

    def __eq__(self, other) -> bool:
        """
        __eq__ is needed to make StateNode comparable and usable in Sets/Dicts
        This implementation simply checks types and then compares get_all_features().

        You probably want to leave this function alone in subclasses, but
        it could theoretically be overridden to be more efficient.
        """
        if isinstance(other, type(self)) :
            return self.get_features() == other.get_features()
        raise NotImplementedError
    
    def __hash__(self) -> int:
        """
        Leave this function alone; it is important to make StateNode hashable and usable in Sets/Dicts.
        """
        return hash(self.get_all_features())
