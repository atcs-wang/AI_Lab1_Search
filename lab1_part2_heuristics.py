from roomba_state import FLOOR, CARPET, WALL, GOAL

#### Lab 1, Part 2a: Heuristics #################################################

""" A very unhelpful heuristic. Returns 0"""
def zero_heuristic(state):
    return 0

"""
A heuristic for RoombaRouteState: assuming there is only
one dirty tile (single goal), return the manhattan distance to that dirty tile.
"""
def roomba_manhattan_onegoal(roomba_state):
    grid = roomba_state.get_grid()
    pos_r, pos_c = roomba_state.get_position()

    for r in range(roomba_state.get_height()):
        for c in range(roomba_state.get_width()):
            if grid[r][c] == GOAL : # Find the goal position
                # Return manhattan distance between roomba and goal
                return abs(r - pos_r) + abs(c - pos_c)

    return 0 # in case no goal space left, then done

"""
Next, implement these two heuristic functions for SlidePuzzleStates.
"""

""" Return the Hamming distance (number of tiles out of place) of the SlidePuzzleState """
def slidepuzzle_hamming(puzzle_state):
    score = 0
    n = puzzle_state.size()
    for row in range(n):
        for col in range(n):
            tile = puzzle_state.tile_at(row,col)
            if (tile != 0) and (tile != (row*n + col)) :
                score += 1
    return score

""" Return the sum of Manhattan distances between tiles and goal of the SlidePuzzleState """
def slidepuzzle_manhattan(puzzle_state):
    score = 0
    n = puzzle_state.size()
    for row in range(n):
        for col in range(n):
            tile = puzzle_state.tile_at(row,col)
            if (tile != 0) :
                row_dist = abs((tile // n) - row)
                col_dist = abs((tile % n) - col)
                score += row_dist + col_dist
    return score


# Make updates to RoombaRouteState in roomba_state.py
# to accomodate multiple dirt spots that all must be cleaned.

def roomba_multi_heuristic(roomba_state):
    # TODO
    # My basic attempt, but of course many possible solutions.
    return roomba_distance_to_closest(roomba_state) + max(
        roomba_manhattan_bounding_box(roomba_state),
        roomba_remaining_count(roomba_state) - 1)

def roomba_remaining_count(roomba_state):
    # TODO
    # Admissible and consistent
    return len(roomba_state.get_dirt_locations())

def roomba_distance_to_closest(roomba_state):
    # TODO
    # Admissible, but not consistent!
    locs = roomba_state.get_dirt_locations()
    if len(locs) == 0:
        return 0
    pos_r, pos_c = roomba_state.get_position()
    # get list of manhattan distance to each goal
    manhats = [abs(r - pos_r) + abs(c - pos_c) for r,c in locs]
    # min of the following:
    return min(manhats)

def roomba_distance_to_closest_plus_count(roomba_state):
    # TODO
    # Admissible, but not Consistent?
    return roomba_distance_to_closest(roomba_state) + roomba_remaining_count(roomba_state) - 1

def roomba_distance_to_closest_plus_count_weighted(roomba_state):
    # TODO
    # Admissible, but not Consistent?
    return max (roomba_distance_to_closest(roomba_state) / (roomba_state.get_width() + roomba_state.get_height())
                + roomba_remaining_count(roomba_state) - 1,
                0)

def roomba_manhattan_bounding_box(roomba_state):
    #
    # Admissible, but not Consistent?
    locs = roomba_state.get_dirt_locations()
    if len(locs) == 0:
        return 0
    pos_r, pos_c = roomba_state.get_position()

    rows = [r for r,c in locs]
    max_r, min_r = max(rows), min(rows)
    cols = [c for r,c in locs]
    max_c, min_c = max(cols), min(cols)
    return (max_c - min_c) + (max_r - min_r)

def roomba_manhattan_bounding_box(roomba_state):
    #
    # Admissible, but not Consistent?
    locs = roomba_state.get_dirt_locations()
    if len(locs) == 0:
        return 0
    pos_r, pos_c = roomba_state.get_position()

    rows = [r for r,c in locs]
    max_r, min_r = max(rows), min(rows)
    cols = [c for r,c in locs]
    max_c, min_c = max(cols), min(cols)
    return (max_c - min_c) + (max_r - min_r)

def roomba_distance_to_closest_plus_bounding_box(roomba_state):
    # TODO
    # Admissible, also consistent?
    return roomba_distance_to_closest(roomba_state) + roomba_manhattan_bounding_box(roomba_state)

def roomba_distance_to_farthest(roomba_state):
    # TODO
    # Admissible, but not consistent!
    locs = roomba_state.get_dirt_locations()
    if len(locs) == 0:
        return 0
    pos_r, pos_c = roomba_state.get_position()
    # get list of manhattan distance to each goal
    manhats = [abs(r - pos_r) + abs(c - pos_c) for r,c in locs]
    # min of the following:
    return max(manhats)


all_multi_heuristics = {"Remaining ": roomba_remaining_count,
                        "Closest Dist": roomba_distance_to_closest,
                        "Farthest Dist" : roomba_distance_to_farthest,
                        "Closest + #Remain" : roomba_distance_to_closest_plus_count,
                        "Closest + #Remain Wtd" : roomba_distance_to_closest_plus_count_weighted,
                        "Bounding Box" : roomba_manhattan_bounding_box,
                        "Closest + Bounding Box" : roomba_distance_to_closest_plus_bounding_box,
                        "MAX of all": roomba_multi_heuristic}
