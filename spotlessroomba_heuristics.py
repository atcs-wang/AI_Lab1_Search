from search_heuristics import *
from spotlessroomba_problem import *

INF = float('inf')


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
    pos_r, pos_c = state.position
    # get list of 
    # min of manhattan distance to each dirty:
    return min(abs(r - pos_r) + abs(c - pos_c) for r,c in locs)

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
    
    rows = [r for r,c in locs]
    max_r, min_r = max(rows), min(rows)
    cols = [c for r,c in locs]
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
    pos_r, pos_c = state.position
    # get list of manhattan distance to each goal
    manhats = [abs(r - pos_r) + abs(c - pos_c) for r,c in locs]
    # min of the following:
    return max(manhats)


def roomba_multi_heuristic(state : SpotlessRoombaState) -> float:
    # TODO
    # My basic attempt, but of course many possible solutions.
    return roomba_distance_to_closest(state) + max(
        roomba_manhattan_bounding_box(state),
        roomba_remaining_count(state) - 1)

SPOTLESSROOMBA_HEURISTICS = {"Zero" : zero_heuristic,
                        "Remaining ": roomba_remaining_count,
                        "Closest Dist": roomba_distance_to_closest,
                        "Farthest Dist" : roomba_distance_to_farthest,
                        "Closest + #Remain" : roomba_distance_to_closest_plus_count,
                        "Closest + #Remain Wtd" : roomba_distance_to_closest_plus_count_weighted,
                        "Bounding Box" : roomba_manhattan_bounding_box,
                        "Closest + Bounding Box" : roomba_distance_to_closest_plus_bounding_box,
                        "MAX of all": roomba_multi_heuristic}
