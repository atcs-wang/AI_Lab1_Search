from typing import Dict, Type

from search_algorithms import *

""" Tree Search"""

class TreeRandomSearch(TreeSearchAlgorithmMixin, RandomSearch): 
    pass

class TreeDFS(TreeSearchAlgorithmMixin, DepthFirstSearch): 
    pass

class TreeBFS(TreeSearchAlgorithmMixin, BreadthFirstSearch): 
    pass

class TreeUCS(TreeSearchAlgorithmMixin, UniformCostSearch): 
    pass

class TreeGreedyBest(TreeSearchAlgorithmMixin, GreedyBestSearch): 
    pass

class TreeAStar(TreeSearchAlgorithmMixin, AStarSearch): 
    pass

""" Graph Search"""

class GraphRandomSearch(GraphSearchAlgorithmMixin, RandomSearch): 
    pass

class GraphDFS(GraphSearchAlgorithmMixin, DepthFirstSearch): 
    pass

class GraphBFS(GraphSearchAlgorithmMixin, BreadthFirstSearch): 
    pass

class GraphUCS(GraphSearchAlgorithmMixin, UniformCostSearch): 
    pass

class GraphGreedyBest(GraphSearchAlgorithmMixin, GreedyBestSearch): 
    pass

class GraphAStar(GraphSearchAlgorithmMixin, AStarSearch): 
    pass

""" Anytime Search"""

class AnytimeRandomSearch(AnytimeSearchAlgorithmMixin, RandomSearch): 
    pass

class AnytimeDFS(AnytimeSearchAlgorithmMixin, DepthFirstSearch): 
    pass

class AnytimeBFS(AnytimeSearchAlgorithmMixin, BreadthFirstSearch): 
    pass

class AnytimeUCS(AnytimeSearchAlgorithmMixin, UniformCostSearch): 
    pass

class AnytimeGreedyBest(AnytimeSearchAlgorithmMixin, GreedyBestSearch): 
    pass

class AnytimeAStar(AnytimeSearchAlgorithmMixin, AStarSearch): 
    pass



ALL_AGENTS : Dict[str, Dict[str, Type[GoalSearchAgent] ]] = {
    "tree" : {
        "random": TreeRandomSearch,
        "dfs": TreeDFS,
        "bfs": TreeBFS,
        "ucs": TreeUCS,
        "greedy": TreeGreedyBest,
        "astar": TreeAStar,
    },
    "graph" : {
        "random": GraphRandomSearch,
        "dfs": GraphDFS,
        "bfs": GraphBFS,
        "ucs": GraphUCS,
        "greedy": GraphGreedyBest,
        "astar": GraphAStar,
    },
    "anytime" : {
        "random": AnytimeRandomSearch,
        "dfs": AnytimeDFS,
        "bfs": AnytimeBFS,
        "ucs": AnytimeUCS,
        "greedy": AnytimeGreedyBest,
        "astar": AnytimeAStar,
    }
}