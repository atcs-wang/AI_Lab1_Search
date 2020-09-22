from search_heuristics import *
from slidepuzzle_problem import *

INF = float('inf')

#### Lab 1, Part 2a: Heuristics #################################################

"""
Next, implement these two heuristic functions for SlidePuzzleStates.
"""

""" Return the Hamming distance (number of tiles out of place) of the SlidePuzzleState """
def slidepuzzle_hamming(state : SlidePuzzleState)  -> float:
    score = 0
    n = state.get_size()
    for row in range(n):
        for col in range(n):
            tile = state.get_tile_at(Coordinate(row,col))
            if (tile != 0) and (tile != (row*n + col)) :
                score += 1
    return score

""" Return the sum of Manhattan distances between tiles and goal of the SlidePuzzleState """
def slidepuzzle_manhattan(state : SlidePuzzleState)  -> float:
    score = 0
    n = state.get_size()
    for row in range(n):
        for col in range(n):
            tile = state.get_tile_at(Coordinate(row,col))
            if (tile != 0) :
                row_dist = abs((tile // n) - row)
                col_dist = abs((tile % n) - col)
                score += row_dist + col_dist
    return score


# This is a named list of heuristics for the Roomba problem.
# Add any more that you wish to use in the GUI
SLIDEPUZZLE_HEURISTICS = {
    "Zero" : zero_heuristic, 
    "Arbitrary": arbitrary_heuristic, 
    "Hamming" : slidepuzzle_hamming,
    "Manhattan" : slidepuzzle_manhattan
    }

