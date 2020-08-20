from __future__ import annotations
from typing import Optional, Tuple, Dict, Any, Hashable, Sequence, Iterable

from statenode import StateNode
from roomba_state import *


DIRTY_FLOOR : LayoutConstant = '?'
DIRTY_CARPET : LayoutConstant = '+'

DIRTY_CONST = {FLOOR : DIRTY_FLOOR, CARPET : DIRTY_CARPET}
CLEAN_CONST = {DIRTY_FLOOR : FLOOR, DIRTY_CARPET : CARPET}

class RoombaMultiRouteState(RoombaRouteState):
    """
    A subclass of RoombaRouteState. The main difference is that the roomba agent's goal is to 
    reach (and clean) ALL the dirty spots, not just one of them.
    """

    dirty_locations : Tuple[Coordinate,...]

    #Overridden
    @staticmethod
    def readFromFile(filename : str) -> RoombaRouteMultiState:
        """Reads data from a text file and returns a RoombaMultiRouteState which is an initial state.
        """
        with open(filename, 'r') as file:
            # This first part is the same as the RoombaRouteState...

            # First line has the number of rows and columns
            max_r, max_c = (int(x) for x in file.readline().split())
            # Second line has the initial row/column of the roomba agent
            init_r, init_c = (int(x) for x in file.readline().split())
            # Remaining lines are the layout grid of 
            grid = tuple( tuple(line.split()) for line in file.readlines())
            # Sanity check - is the grid really the right size?
            assert (len(grid) == max_r and all( len(row) == max_c for row in grid))

            # Once again, the grid itself is effectively the same for each state, 
            # except now we must keep track of which dirty spots have been cleaned or not yet.
            # Instead of updating the grid from state to state, 
            # we will instead keep a list (tuple) of which of the locations are still dirty. 
            # This makes tracking the differences between states easier, faster, 
            # and more memory efficient, among other advantages.
            dirty = []
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if self.grid[i][j] in (DIRTY_CARPET, DIRTY_FLOOR):
                        dirty.add((i,j))

            # Now re-do the grid with the dirty spots changed to their clean counterparts
            grid = tuple( tuple(CLEAN_CONST.get(x, x) for x in row) for row in grid)

            return RoombaRouteMultiState(dirty_locations = tuple(dl),
                                position = (init_r, init_c),
                                grid = grid,
                                parent = None,
                                last_action = None,
                                path_length = 0,
                                path_cost = 0)


    def __init__(self, 
                dirty_locations : Tuple[Coordinate,...],
                position: Tuple[int, int], 
                grid: Tuple[Tuple[LayoutConstant,...],...], 
                parent : Optional[RoombaMultiRouteState], 
                last_action: Optional[Coordinate],  #Note that actions are (relative) Coordinates!
                path_length : int, 
                path_cost : float = 0.0) :
        """
        Creates a RoombaMultiRouteState, which represents a state of the roomba's environment .

        Keyword Arguments (in addition to RoombaRouteState arguments):
        dirty_locations -- A tuple of all the not-yet cleaned (visited) locations that are (still) dirty in the grid. 
        """
        super().__init__(position = position, grid = grid, parent = parent, last_action = last_action, path_length = path_length, path_cost = path_cost)
        self.dirty_locations = dirty_locations
        


    """ Overridden methods from RoombaRouteState and StateNode """
   
    # Override
    def get_all_features(self) :
        """Returns a full feature representation of the state.

        Once again, the grid  is essentially the same for each state, except we must 
        keep track of which dirty spots have been cleaned or not yet.

        Therefore, we'll use dirty_locations as a feature (plus roomba agent position), since it captures the 
        difference between two states sufficiently. Note that this is far more time and memory efficient 
        than using the whole grid as a feature, which must be updated for each state.

        If two RoombaMultiRouteStateNode objects represent the same state, get_features() should return the same for both objects.
        Note, however, that two states with identical features may have been arrived at from different paths.
        """
        return (self.get_position(), self.dirty_locations) 

    # Override
    def __str__(self) -> str:
        """Return a string representation of the state."""
        s = list(super().__str__()) 
        # Draw all dirty spots 
        for r, c in self.dirty_locations:
            pos = r * (self.get_width()+1) + self.get_col()
            s[pos]+ DIRTY_CONST.get(s[pos],s[pos])
        return str(s)

    # Override
    def is_goal_state(self) -> bool:
        """Returns if a goal (terminal) state.
        If there are no more dirty locations, the roomba has finished cleaning!
        """
        return len(self.dirty_locations) == 0

    # Override
    def get_next_state(self, action : Any) -> RoombaMultiRouteState:
        """ Return a new RoombaRouteState that represents the state that results from taking the given action from this state.
        The new RoombaRouteState object should have this (self) as its parent, and action as its last_action.

        -- action is assumed legal (is_legal_action called before)
        """
        new_pos = add(self.position, action)
        step_cost = RoombaRouteState.TRANSITION_COSTS[self.get_terrain(new_pos)]
        # If moving onto a dirty spot, it gets cleaned!
        return RoombaRouteState( 
            dirty_locations = tuple(list(self.dirty_locations).remove(new_pos)) 
                                if new_pos in dirty_locations 
                                else self.dirty_locations,
            position = new_pos,
            grid = grid, 
            last_action = action,
            parent = self,
            path_length = self.path_length + 1,
            path_cost = self.path_cost + step_cost)

