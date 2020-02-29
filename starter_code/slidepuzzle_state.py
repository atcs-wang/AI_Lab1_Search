# Lab 1, Part 1b: Problem Representation.
# Name(s):

from statenode import StateNode

#### Lab 1, Part 1b: Problem Representation #################################################

class SlidePuzzleState(StateNode):

    """
    A 'static' method that reads mazes from text files and returns
    a SlidePuzzleState which is an initial state.
    """
    # Override
    def readFromFile(filename):
        raise NotImplementedError

    """
    Creates a SlidePuzzleState node.
    Takes:

        ADDITIONAL PARAMETERS OF YOUR DESIGN

    parent: the preceding StateNode along the path taken to reach the state
            (the initial state's parent should be None)
    path_length, the number of actions taken in the path to reach the state
    path_cost (optional), the cost of the entire path to reach the state
    """
    def __init__(self, parent, path_length, path_cost = 0, empty_pos = None) :
        super().__init__(parent, path_length, path_cost)
        raise NotImplementedError


    """
    Returns the dimension N of the square puzzle represented which is N-by-N.
    Needed by the GUI, should be FAST
    """
    def size(self) :
        raise NotImplementedError

    """
    Returns the number at the tile at the given row and col (starting from 0).
    If the empty tile, return 0.
    Needed by the GUI, should be FAST
    """
    def tile_at(self, row, col) :
        raise NotImplementedError

    """
    Returns a 2-tuple (row, col) of coordinates of the empty tile.
    Needed by the GUI, should be FAST
    """
    def get_empty_pos(self):
        raise NotImplementedError


    """
    Returns a full feature representation of the environment's current state.
    This should be an immutable type - only primitives, strings, and tuples.
    (no lists or objects).
    If two StateNode objects represent the same state,
    get_features() should return the same for both objects.
    Note, however, that two states with identical features
    may have different paths.
    """
    # Override
    def get_all_features(self) :
        raise NotImplementedError

    """
    Returns True if a goal state.
    """
    # Override
    def is_goal_state(self) :
        raise NotImplementedError

    """
    Return a string representation of the State
    This gets called when str() is used on an Object.
    """
    # Override
    def __str__(self):
        raise NotImplementedError


    """
    Returns a string describing the action taken from the parent StateNode
    that results in transitioning to this StateNode
    along the path taken to reach this state.
    (None if the initial state)
    """
    # Override
    def describe_previous_action(self) :
        raise NotImplementedError

    """
    Generate and return an iterable (e.g. a list) of all possible neighbor
    states (StateNode objects).
    """
    # Override
    def generate_next_states(self) :
        raise NotImplementedError

    """ You may add additional methods that may be useful! """
