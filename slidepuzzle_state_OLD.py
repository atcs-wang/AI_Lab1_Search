from __future__ import annotations
from typing import Optional, Tuple, Dict, Any, Hashable, Sequence, Iterable

from statenode import StateNode

Coordinate = TypeVar('Coordinate', bound=Tuple[int,int])


class SlidePuzzleState(StateNode):
    # A class-level variable (static) representing all the directions
    # the empty position can move.
    NEIGHBORING_STEPS = {(0,1): " LEFT", (1,0): " UP", (0, -1): " RIGHT", (-1,0): " DOWN"}

   
    @staticmethod
    def readFromFile(filename : str) -> SlidePuzzleState:
        """Reads data from a text file and returns a SlidePuzzleState which is an initial state."""
        with open(filename, 'r') as file:
            tiles = []
            n = None

            n = int(file.readline())
            for i in range(n):
                row = [int(x) for x in file.readline().split()]
                tiles.append(row)

        return SlidePuzzleState( tiles = tiles,
                            last_action = None,
                            parent = None,
                            path_length = 0,
                            path_cost = 0,
                            empty_pos = None)

    """
    Creates a maze state node.
    Takes:
    tiles: 2-d grid of board layout (will be deep copied)
    last_action: string describing the last action taken
    OPTIONAL empty_pos: 2-tuple coordinates of empty tile.

    parent: the preceding StateNode along the path taken to reach the state
            (the initial state's parent should be None)
    path_length, the number of actions taken in the path to reach the state
    path_cost (optional), the cost of the entire path to reach the state
    """
    def __init__(self, tiles, last_action, parent, path_length, path_cost = 0, empty_pos = None) :
        super().__init__(parent, path_length, path_cost)

        self.tiles = tuple([tuple(row) for row in tiles])
        self.last_action = last_action
        self.empty_pos = empty_pos
        if empty_pos == None:
            self.empty_pos = self.indexesOf(0)

    def indexesOf(self, n):
        for r, row in enumerate(self.tiles):
            for c, i in enumerate(row):
                if n == i:
                    return (r,c)

    def size(self) :
        return len(self.tiles)

    def tile_at(self, row, col) :
        return self.tiles[row][col]

    def get_empty_pos(self):
        return self.empty_pos

    """
    Returns a full feature representation of the environment's current state.
    This should be an immutable type - namely primitives, strings, and tuples.
    (no lists or objects).
    If two StateNode objects represent the same state,
    get_features() should return the same for both objects.
    Note, however, that two states with identical features
    may have different paths.
    """
    # Override
    def get_all_features(self) :
        return self.tiles

    """
    Returns True if a goal state.
    """
    # Override
    def is_goal_state(self) :
        n = 0
        for r in range(self.size()):
            for c in range(self.size()):
                if self.tile_at(r,c) != n:
                    return False
                n += 1
        return True

    """
    Return a string representation of the State
    This gets called when str() is used on an Object.
    """
    # Override
    def __str__(self):
        str_list = []

        for row in range(self.size()):
            for col in range(self.size()):
                str_list.append("{:3d}".format(self.tile_at(row,col)))
            str_list.append("\n")
        return "".join(str_list)



    """
    Returns a string describing the action taken from the parent StateNode
    that results in transitioning to this StateNode
    along the path taken to reach this state.
    (None if the initial state)
    """
    def describe_previous_action(self) :
        return self.last_action

    """
    Generate and return an iterable (e.g. a list) of all possible neighbor
    states (StateNode objects).
    If avoid_backtrack is True, don't include the parent state in the iterable.
    """
    # Override
    def generate_next_states(self) :
        listgrid = [list(row) for row in self.tiles]
        n = len(listgrid);
        nbs = []

        blank_y, blank_x = self.empty_pos

        for dy, dx in SlidePuzzleState.NEIGHBORING_STEPS:
            swap_y = dy + blank_y
            swap_x = dx + blank_x
            if swap_x >= 0 and  swap_x < n and swap_y >= 0 and  swap_y < n:

                listgrid[blank_y][blank_x] = listgrid[swap_y][swap_x]
                listgrid[swap_y][swap_x] = 0
                nbs.append(SlidePuzzleState(tiles = listgrid,
                    last_action = str(listgrid[blank_y][blank_x]) + SlidePuzzleState.NEIGHBORING_STEPS[(dy,dx)],
                    parent = self,
                    path_length = self.path_length + 1,
                    path_cost = self.path_cost + 1,
                    empty_pos = (swap_y, swap_x)
                    ))
                listgrid[swap_y][swap_x] = listgrid[blank_y][blank_x]
                listgrid[blank_y][blank_x] = 0

        return nbs


    """ You may add additional methods that may be useful! """
