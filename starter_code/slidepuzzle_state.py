# Lab 1, Part 1b: Problem Representation.
# Name(s):
from __future__ import annotations
from typing import Optional, Tuple, Dict, Any, Hashable, Sequence, Iterable

from statenode import StateNode

Coordinate = TypeVar('Coordinate', bound=Tuple[int,int])

#### Lab 1, Part 1b: Problem Representation #################################################

"""
A state node for the slide puzzle environment.
"""
class SlidePuzzleState(StateNode):

    """ Type Hints allow for the optional type declaration of "instance variables" this way, like Java.
        It is recommended you list them here:
    """
    # TODO Declare instance variables, like:
    # variable : type
    
    @staticmethod
    def readFromFile(filename : str) -> StateNode:
        """Reads data from a text file and returns a SlidePuzzleState which is an initial state."""
        with open(filename, 'r') as file:
            # TODO Read from the text file according to the following format:
            # The first line indicates N, the dimension of the square puzzle (number of rows and columns)
            # The next N lines have N numbers each, separated by whitespace,
            # representing the initial position of the various tiles. 0 represents
            # the empty space with no tile.
            raise NotImplementedError

    def __init__(self, 
                parent : Optional[StateNode], 
                last_action: Optional[Any], 
                path_length : int, 
                path_cost : float = 0.0) :
        """Creates a SlidePuzzleState that represents a state of the environment and context for how the agent gets 
        to this state (the path, aka a series of state-action transitions).
        
        Keyword Arguments:
        All the arguments for StateNode's __init__; Use super.__init__() to call this function and pass appropriate parameters.
        # TODO Add more additional parameters that help define its state features.
        """
        super().__init__(parent = parent, last_action = last_action, path_length = path_length, path_cost = path_cost)
        # TODO set up additional instance variables

    """ Additional accessor methods - needed for the GUI"""

    def get_size(self) -> int:
        """Returns the dimension N of the square puzzle represented which is N-by-N."""
        # TODO
        raise NotImplementedError

    def get_tile_at(self, coord : Coordinate) -> int:
        """ Returns the number of the tile at the given Coordinate (2-tuple of (row, col)) .
        If the position is empty, return 0.
        Ideally, this should be done in constant time, not O(N) or O(N^2) time...
        """
        # TODO
        raise NotImplementedError

    def get_empty_pos(self) -> Coordinate:
        """Returns Coordinate (2-tuple of (row, col)) of the empty tile.
        Ideally, this should be done in constant time, not O(N) or O(N^2) time...
        """
        # TODO
        raise NotImplementedError

    """ Overridden methods from StateNode """

    # Override
    def get_all_features(self) -> Hashable:
        """Returns a full featured representation of the state.

        This should return something consistent, immutable, and hashable - primitives, strings, and tuples of such (generally no lists or objects).
                
        If two SlidePuzzleState objects represent the same state, get_features() should return the same for both objects.
        Note, however, that two states with identical features may have been arrived at from different paths.
        """
        # TODO
        raise NotImplementedError

    # Override
    def __str__(self) -> str:
        """Return a string representation of the state.
           
           This should return N lines of N numbers each, separated by whitespace,
           similar to the file format for initial states
        """
        # TODO
        raise NotImplementedError

    # Override
    def is_goal_state(self) -> bool:
        """Returns if a goal (terminal) state. 
        The goal of the slide puzzle is to have the empty spot in the 0th row and col,
        and then the rest of the numbered tiles in row-major order!
        """
        # TODO
        raise NotImplementedError

    # Override
    def is_legal_action(self, action : Any) -> bool:
        """Returns whether an action is legal from the current state

        Actions in the slide puzzle environment involve moving a tile into
        the adjacent empty spot.
        It is up to the coder to define a datatype for representing actions,
        and also then what constitutes a legal action in a state.
        # TODO Add a comment describing the action type and what makes it legal.
        """
        # TODO
        raise NotImplementedError

    # Override
    def get_all_actions(self) -> Iterable[Any]:
        """Return all legal actions at this state."""
        # TODO
        raise NotImplementedError

    # Override
    def describe_last_action(self) -> str:
        """Returns a string describing the last_action taken (that resulted in transitioning from parent to this state)
        (Can be None or "None" if the initial state)

        The action should be described as "Moved tile X" where X is the tile number
        that last got slid into the empty spot.
        """
        # TODO
        raise NotImplementedError

    # Override
    def get_next_state(self, action : Any) -> StateNode:
        """ Return a new StateNode that represents the state that results from taking the given action from this state.
        The new StateNode object should have this StateNode (self) as its parent, and action as its last_action.

        -- action is assumed legal (is_legal_action called before), but a ValueError may be passed for illegal actions if desired.
        """
        raise NotImplementedError

    """ You may add additional methods that may be useful! """
