from search_heuristics import *
from spotlessroomba_problem import *

def roomba_remaining_count(state : SpotlessRoombaState)  -> float:
    # TODO
    # Admissible and consistent
    return len(state.dirty_locations)

def roomba_distance_to_closest(state : SpotlessRoombaState)  -> float:
    # TODO
    # Admissible, but not consistent!
    locs = state.dirty_locations
    if len(locs) == 0:
        return 0
    # get list of 
    # min of manhattan distance to each dirty:
    return min(abs(dirt.row - state.position.row) + abs(dirt.col - state.position.col) for dirt in locs)

def roomba_distance_to_closest_plus_count(state : SpotlessRoombaState)  -> float:
    # TODO
    # Admissible, but not Consistent?
    return roomba_distance_to_closest(state) + roomba_remaining_count(state) - 1

def roomba_distance_to_closest_plus_count_weighted(state : SpotlessRoombaState)  -> float:
    # TODO
    # Admissible, but not Consistent?
    return roomba_distance_to_closest(state) + (state.get_width() + state.get_height()) * max(roomba_remaining_count(state) - 1, 0)

def roomba_manhattan_bounding_box(state : SpotlessRoombaState)  -> float:
    #
    # Admissible, but not Consistent?
    locs = state.dirty_locations
    if len(locs) == 0:
        return 0
    
    rows = [c.row for c in locs]
    max_r, min_r = max(rows), min(rows)
    cols = [c.col for c in locs]
    max_c, min_c = max(cols), min(cols)
    return (max_c - min_c) + (max_r - min_r)

def roomba_distance_to_closest_plus_bounding_box(state : SpotlessRoombaState) -> float:
    # TODO
    # Admissible, also consistent?
    return roomba_distance_to_closest(state) + roomba_manhattan_bounding_box(state)

def roomba_distance_to_farthest(state : SpotlessRoombaState)  -> float:
    # TODO
    # Admissible, but not consistent!
    locs = state.dirty_locations
    if len(locs) == 0:
        return 0
    # get max of list of manhattan distances to each goal
    return max(abs(dirt.row - state.position.row) + abs(dirt.col - state.position.col) for dirt in locs)


def roomba_multi_heuristic(state : SpotlessRoombaState) -> float:
    # TODO
    # My basic attempt, but of course many possible solutions.
    return roomba_distance_to_closest(state) + max(
        roomba_manhattan_bounding_box(state),
        roomba_remaining_count(state) - 1)

SPOTLESSROOMBA_HEURISTICS = {"Zero" : zero_heuristic,
                        "Arbitrary": arbitrary_heuristic, 
                        "A" : roomba_remaining_count, 
                        "B": roomba_distance_to_closest,
                        "C" : roomba_distance_to_farthest,
                        "D" : roomba_distance_to_closest_plus_count,
                        "E" : roomba_distance_to_closest_plus_count_weighted,
                        "F" : roomba_manhattan_bounding_box,
                        "G" : roomba_distance_to_closest_plus_bounding_box,
                        "H": roomba_multi_heuristic}

# SPOTLESSROOMBA_HEURISTICS = {"Zero" : zero_heuristic,
                        # "Arbitrary": arbitrary_heuristic, 
#                         "Remaining" : roomba_remaining_count, 
#                         "Closest Dist": roomba_distance_to_closest,
#                         "Farthest Dist" : roomba_distance_to_farthest,
#                         "Closest + #Remain" : roomba_distance_to_closest_plus_count,
#                         "Closest + #Remain Wtd" : roomba_distance_to_closest_plus_count_weighted,
#                         "Bounding Box" : roomba_manhattan_bounding_box,
#                         "Closest + Bounding Box" : roomba_distance_to_closest_plus_bounding_box,
#                         "MAX of all": roomba_multi_heuristic}
