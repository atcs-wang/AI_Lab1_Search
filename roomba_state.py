from __future__ import annotations
from typing import Optional, Tuple, Dict, Any, Hashable, Sequence, Iterable

from statenode import StateNode
LayoutConstant = TypeVar('LayoutConstant', bound=str)
Coordinate = TypeVar('Coordinate', bound=Tuple[int,int])

FLOOR : LayoutConstant = '.'
CARPET  : LayoutConstant = '~'
WALL : LayoutConstant = '#'
GOAL : LayoutConstant = '?'


class RoombaRouteState(StateNode):
    """
    An immutable representation of the state of a Roomba Route environment. 
    In such an environment, the roomba moves around a grid with the goal of 
    finding the (or a) dirty spot to clean. 
    """

    """A class-level variable representing all the directions the position can move."""
    NEIGHBORING_STEPS : Dict[Coordinate, str] = {(0,1): "East", (1,0): "South", (0, -1): "West", (-1,0): "North"}
    """A class-level variable representing the cost to move onto different types of terrain."""
    TRANSITION_COSTS : Dict[LayoutConstant, float]= {FLOOR: 1, CARPET: 2, WALL: 0, GOAL: 1}

    """ Type Hints allow for the optional type declaration of "instance variables" this way, like Java """
    position : Coordinate
    grid : Tuple[Tuple[LayoutConstant,...],...]

    #Override
    @staticmethod
    def readFromFile(filename : str) -> RoombaRouteState:
        """Reads data from a text file and returns a RoombaRouteState which is an initial state."""
        with open(filename, 'r') as file:
            # First line has the number of rows and columns in the environment's grid
            max_r, max_c = (int(x) for x in file.readline().split())
            # Second line has the initial row/column of the roomba agent
            init_r, init_c = (int(x) for x in file.readline().split())
            # Remaining lines are the layout grid of the environment
            grid = tuple( tuple(line.split()) for line in file.readlines())
            # Sanity check - is the grid really the right size?
            assert (len(grid) == max_r and all( len(row) == max_c for row in grid))

            return RoombaRouteState(position = (init_r, init_c),
                                grid = grid,
                                parent = None,
                                last_action = None,
                                path_length = 0,
                                path_cost = 0)
    
    #Override
    def __init__(self, 
                position: Tuple[int, int], 
                grid: Tuple[Tuple[LayoutConstant,...],...], 
                parent : Optional[RoombaRouteState], 
                last_action: Optional[Coordinate],  #Note that actions are (relative) Coordinates!
                path_length : int, 
                path_cost : float = 0.0) :
        """
        Creates a RoombaRouteState, which represents a state of the roomba's environment .

        Keyword Arguments (in addition to StateNode arguments):
        position: Tuple of roomba agent's current row/col coordinates
        grid: 2-d Tuple grid of LayoutConstants, representing the maze.
        """
        super().__init__(parent = parent, last_action = last_action, path_length = path_length, path_cost = path_cost)
        self.position = position
        self.grid = grid


    """ Additional accessor methods """
    
    def get_width(self) -> int:
        """Returns the width (number of cols) of the maze"""
        return len(self.grid[0])

    def get_height(self) -> int:
        """Returns the height (number of rows) of the maze"""
        return len(self.grid)

    def get_row(self) -> int:
        """Returns the row of the roomba's current position in the maze"""
        return position[0]

    def get_col(self) -> int:
        """Returns the row of the roomba's current position in the maze"""
        return position[1]

    def is_inbounds(self, coord : Coordinate) -> bool:
        return (coord[0] >= 0) and (coord[1]  >= 0) and (coord[0] < self.get_height()) and (coord[1] < self.get_width())
    
    def get_terrain(self, coord : Coordinate) -> LayoutConstant:
        return self.grid[coord[0]][coord[1]]

    @staticmethod
    def add(c1 : Coordinate, c2 : Coordinate) -> Coordinate:
        return (c1[0] + c2[0], c1[1] + c2[1])

    """ Overridden methods from StateNode """

    # Override
    def get_all_features(self) -> Hashable:
        """Returns a full feature representation of the state.
        Since the grid is the same for all possible states in this environment
        the position alone is sufficient to distinguish between states.

        If two RoombaRouteState objects represent the same state, this should return the same for both objects.
        Note, however, that two states with identical features may have been arrived at from different paths.
        """
        return (self.position)

    # Override
    def __str__(self) -> str:
        """Return a string representation of the state."""
        s = "\n".join("".join(row) for row in self.grid)
        ## Draw the roomba agent at the correct position.
        pos = self.get_row() * (self.get_width()+1) + self.get_col()
        return s[:pos] + 'X' + s[pos+1:] + "\n" # 

    # Override
    def is_goal_state(self) -> bool:
        """Returns if a goal (terminal) state."""
        return self.get_terrain(self.position) == GOAL

    # Override
    def is_legal_action(self, action : Coordinate) -> bool:
        """Returns whether an action is legal from the current state"""
        newpos = add(self.position, action)
        return self.is_inbounds(newpos) and self.get_terrain(newpos) != WALL

    # Override
    def get_all_actions(self) -> Iterable[Coordinate]:
        """Return all legal actions from this state. Actions are (relative) Coordinates."""
        for action in self.NEIGHBORING_STEPS.keys :
            if self.is_legal_action(action):
                yield action

    # Override
    def describe_last_action(self) -> str:
        """Returns a string describing the last_action taken (that resulted in transitioning from parent to this state)
        (None if the initial state)
        """
        return self.NEIGHBORING_STEPS.get(self.last_action, None)

    # Override
    def get_next_state(self, action : Any) -> RoombaRouteState:
        """ Return a new RoombaRouteState that represents the state that results from taking the given action from this state.
        The new RoombaRouteState object should have this (self) as its parent, and action as its last_action.

        -- action is assumed legal (is_legal_action called before)
        """
        new_pos = add(self.position, action)
        step_cost = RoombaRouteState.TRANSITION_COSTS[self.get_terrain(new_pos)]
        return RoombaRouteState( position = new_pos,
                                grid = self.grid, # The grid doesn't change from state to state
                                last_action = action,
                                parent = self,
                                path_length = self.path_length + 1,
                                path_cost = self.path_cost + step_cost)