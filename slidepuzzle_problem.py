# Lab 1, Part 1b: Problem Representation.
# Name(s): SOLUTION
from __future__ import annotations
from typing import *

from search_problem import StateNode, Action

#### Lab 1, Part 1b: Problem Representation #################################################

class Coordinate(NamedTuple, Action):
    r : int
    c : int

class SlidePuzzleState(StateNode):
    """ A state node for the slide puzzle environment. """

    """ Type Hints allow for the optional type declaration of "instance variables" this way, like Java.
        It is recommended you list them here:
    """
    # TODO Declare instance variables, like:
    # variable : type
    tiles : Tuple[Tuple[int, ...], ...]
    empty_pos : Coordinate
    
    @staticmethod
    def readFromFile(filename : str) -> StateNode:
        """Reads data from a text file and returns a SlidePuzzleState which is an initial state."""
        with open(filename, 'r') as file:
            n = int(file.readline())
            tiles = tuple( tuple(int(x) for x in file.readline().split()) for i in range(n))
            # look for the zero 
            for r, row in enumerate(tiles):
                for c, i in enumerate(row):
                    if i == 0:
                        return SlidePuzzleState( 
                            tiles = tiles,
                            empty_pos = Coordinate(r,c),
                            parent = None,
                            last_action = None,
                            depth = 0,
                            path_cost = 0,
                            )
            # If we get here, no zero found
            raise ValueError
    
    #Override
    def __init__(self, 
            tiles : Tuple[Tuple[int, ...], ...],
            empty_pos : Coordinate,
            parent : Optional[StateNode], 
            last_action: Optional[Any], 
            depth : int, 
            path_cost : float = 0.0) :
        """Creates a SlidePuzzleState that represents a state of the environment and context for how the agent gets 
        to this state (the path, aka a series of state-action transitions).
        
        Keyword Arguments:
        All the arguments for StateNode's __init__; Use super.__init__() to call this function and pass appropriate parameters.
        tiles -- a tuple grid of integers representing the position of different numbered tiles
        empty_pos -- a coordinate indicating the position of the empty spot (tile 0)
        """
        super().__init__(parent = parent, last_action = last_action, depth = depth, path_cost = path_cost)
        self.tiles = tiles
        self.empty_pos = empty_pos

    """ Additional accessor methods - needed for the GUI"""

    def get_size(self) -> int:
        """Returns the dimension N of the square puzzle represented which is N-by-N."""
        return len(self.tiles)

    def get_tile_at(self, coord : Coordinate) -> int:
        """ Returns the number of the tile at the given Coordinate.
        If the position is empty, return 0.
        Ideally, this should be done in constant time, not O(N) or O(N^2) time...
        """
        return self.tiles[coord[0]][coord[1]]

    def get_empty_pos(self) -> Coordinate:
        """Returns Coordinate of the empty tile.
        Ideally, this should be done in constant time, not O(N) or O(N^2) time...
        """
        return self.empty_pos

    """ Overridden methods from StateNode """

    # Override
    def get_state_features(self) -> Hashable:
        """Returns a full featured representation of the state.
        
        If two SlidePuzzleState objects represent the same state, get_features() should return the same for both objects.
        However, two SlidePuzzleState with identical state features may not represent the same node of the search tree -
        that is, they may have different parents, last actions, path lengths/costs etc...
        """
        return self.tiles

    # Override
    def __str__(self) -> str:
        """Return a string representation of the state.
           
           This should return N lines of N numbers each, separated by whitespace,
           similar to the file format for initial states
        """
        n = self.get_size()
        return "\n".join(" ".join("{:2d}".format(self.tiles[r][c]) for c in range(n)) for r in range(n))
    
    # Override
    def is_goal_state(self) -> bool:
        """Returns if a goal (terminal) state. 
        The goal of the slide puzzle is to have the empty spot in the 0th row and col,
        and then the rest of the numbered tiles in row-major order!
        """
        i = 0
        for r in range(self.get_size()):
            for c in range(self.get_size()):
                if self.tiles[r][c] != i:
                    return False
                i += 1
        return True

    # Override
    def is_legal_action(self, action : Coordinate) -> bool:
        """Returns whether an action is legal from the current state

        Actions in the slide puzzle environment involve moving a tile into
        the adjacent empty spot.
        It is up to the coder to define a datatype for representing actions,
        and also then what constitutes a legal action in a state.
        
        One possible way to represent action is as the Coordinate of the tile that
        is to be moved into the empty slot. It needs to be not out of bounds, and 
        actually adjacent.
        """
        return self.is_inbounds(action) and (
            abs(action[0] - self.empty_pos[0]) + abs(action[1] - self.empty_pos[1])) == 1

    # Override
    def get_all_actions(self) -> Iterable[Coordinate]:
        """Return all legal actions at this state."""
        for dr, dc in ((0,1), (-1,0), (0,-1), (1,0)):
            action = (self.empty_pos[0] + dr, self.empty_pos[1] + dc)
            if self.is_inbounds(action):
                yield action

    # Override
    def describe_last_action(self) -> str:
        """Returns a string describing the last_action taken (that resulted in transitioning from parent to this state)
        (Can be None or "None" if the initial state)

        The action should be described as "Moved tile X" where X is the tile number
        that last got slid into the empty spot.
        """
        if self.last_action is None:
             return None 
        return "Moved tile {}".format(self.parent.get_tile_at(self.last_action))

    # Override
    def get_next_state(self, action : Coordinate) -> SlidePuzzleState:
        """ Return a new StateNode that represents the state that results from taking the given action from this state.
        The new StateNode object should have this StateNode (self) as its parent, and action as its last_action.

        -- action is assumed legal (is_legal_action called before), but a ValueError may be passed for illegal actions if desired.
        """
        # Swap empty_pos with action Coord
        t = self.get_tile_at(action)
        new_tiles = tuple(tuple( 0 if (r,c) == action else (t if (r,c) == self.empty_pos else x) for c, x in enumerate(row)) for r, row in enumerate(self.tiles))
        return SlidePuzzleState( 
                        tiles = new_tiles,
                        empty_pos = action,
                        parent = self,
                        last_action = action,
                        depth = self.depth + 1,
                        path_cost = self.path_cost + 1,
                        )

    """ You may add additional methods that may be useful! """

    def is_inbounds(self, coord : Coordinate) -> bool:
        return (coord[0] >= 0) and (coord[1]  >= 0) and (coord[0] < self.get_size()) and (coord[1] < self.get_size())

    def get_tile_final_dest(self, tile : int) -> Coordinate:
        return (tile // self.get_size(), tile % self.get_size())