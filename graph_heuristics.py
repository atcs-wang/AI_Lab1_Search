from search_heuristics import *
from graph_problem import *

INF = float('inf')

def graph_heuristic(state : GraphState)  -> float:
    return state.heuristics[state.this_state]

# This is a named list of heuristics for the Graph problem.
# Add any more that you wish to use in the GUI
GRAPH_HEURISTICS = {
    "Zero" : zero_heuristic, 
    "Arbitrary": arbitrary_heuristic, 
    "Heuristic": graph_heuristic,
    }

