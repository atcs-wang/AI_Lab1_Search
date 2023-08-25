A educational visualizer for Goal Search algorithms, including
- DFS, BFS, UCS, Greedy-Best search, and A* search.
- tree, graph, limited depth, and anytime variants. 

The goal-search problem model, search algorithms, and visualizer gui and are all abstractly generalized (see files with the `search_` prefix); files with other prefixes refer to concrete environments with problem models and visualizer guis that inherit from the abstract problem/gui, 

These concrete environments include:
- `graph` - abstract graph traversal
- `roomba` - single goal pathfinding
- `spotlessroomba` - multi goal pathfinding
- `slidepuzzle` - classic 8-puzzle style puzzle

To run one of the visualizers, use one of the following commands, with optional command line argument: 

> If the command line argument for the start state file is omitted, you will be prompted with a file selection dialogue, where you must select a file with the appropriate file extension.

```
> python slidepuzzle_gui.py [graph_files/___.graph]
> python roomba_gui.py [roomba_files/___.roomba]
> python spotlessroomba_gui.py [roomba_files/___.roomba]
> python slidepuzzle_gui.py [slidepuzzle_files/___.slidepuzzle]
```

Can be used as an assignment, by replacing any files with versions of the files in the `assignment_starter_files`. 
