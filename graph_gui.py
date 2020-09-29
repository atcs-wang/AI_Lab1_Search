from __future__ import annotations
from typing import *
from tkinter import filedialog, Tk, ARC, N, S
from os import getcwd
from sys import argv
from graph_problem import *
from graph_heuristics import GRAPH_HEURISTICS
from search_algorithms import ALGORITHMS, STRATEGIES
from search_gui import Search_GUI, Search_GUI_Controller

### State visualization too big? Change these numbers
MAX_HEIGHT = 300
MAX_WIDTH = 450

TILE, CURRENT, PATH, TEXT = 'tile', 'CURRENT', 'path', 'text'
TRANSITIONS = 'line'
COLORS = {TILE : 'tan', CURRENT : 'IndianRed1', PATH: 'IndianRed1', TEXT: 'black', TRANSITIONS: 'blue'}

# Use an arc drawing of the graph

class Graph_GUI(Search_GUI):

    current_state : GraphState

    def __init__(self, initial_state : GraphState, algorithm_names : Sequence[str], strategy_names : Sequence[str], heuristics : Dict[str,Callable[[StateNode], float]]):
        self.num_states = len(initial_state.graph)
        self.state_list : List[str] = [x for x in initial_state.graph.keys()]
        super().__init__(canvas_height = MAX_HEIGHT, canvas_width = MAX_WIDTH, algorithm_names = algorithm_names , strategy_names = strategy_names, heuristics = heuristics)
        self.title("Graph Search Visualizer")

    def calculate_box_coords(self, r : int, c : int) -> Tuple[int, int, int, int]:
        w = self.canvas.winfo_width() # Get current width of canvas
        h = self.canvas.winfo_height() # Get current height of canvas
        x1 = w * c // self.num_states
        y1 = h * r // (self.num_states)
        x2 = w * (c + 1) // self.num_states
        y2 = h * (r + 1) // (self.num_states)
        return (x1, y1, x2, y2)

    def calculate_center_coords(self, r : int, c : int) -> Tuple[int, int]:
        w = self.canvas.winfo_width() # Get current width of canvas
        h = self.canvas.winfo_height() # Get current height of canvas
        x = int(w * (c + .5)) // self.num_states
        y = int(h * (r + .5)) // (self.num_states)
        return (x, y)

    def draw_arc_between(self, c1 : int, c2 : int, weight = None, tag = TRANSITIONS, ):
        h = abs(c1 - c2)
        x1, y1 = self.calculate_center_coords(-h, c1)
        x2, y2 = self.calculate_center_coords(h, c2)
        self.canvas.create_arc(x1,y1,x2,y2,start=180, extent=180, width = 3, style=ARC, outline=COLORS[tag], tag=tag)
        if weight:
            if c2 > c1:
                self.canvas.create_text((x1+x2)/2, y2, text= ">{}>".format(weight), fill = COLORS[tag] ,font = ('Times New Roman', self.text_size , 'normal' ), anchor= N, tag= tag)
            else:
                self.canvas.create_text((x1+x2)/2, y2, text="<{}<".format(weight), fill = COLORS[tag] ,font = ('Times New Roman', self.text_size, 'normal' ), anchor= S, tag= tag)

    #Override
    def draw_state(self):
        self.canvas.delete(CURRENT)
        self.canvas.delete(PATH)

        # roomba agent
        c = self.state_list.index(self.current_state.this_state)
            
        # draw CURRENT tile
        coords = self.calculate_box_coords(0,c)
        self.canvas.create_oval(*coords, outline= COLORS[CURRENT], tag=CURRENT)

        if self.current_state.depth > 0:
            self.draw_path()
            self.canvas.tag_raise(TILE)
            self.canvas.tag_raise(TEXT)
    
    #Override
    def draw_path(self):
        path_c = [self.state_list.index(state.this_state)
                        for state in self.current_state.get_path() ]
        for c1, c2 in zip(path_c[:-1], path_c[1:]):
            self.draw_arc_between(c1,c2, self.current_state.graph[self.state_list[c1]][self.state_list[c2]], tag=PATH)

        #do something...
        
    #Override
    def draw_background(self):

        # Clear the background grid and tiles
        self.canvas.delete(TEXT)
        self.canvas.delete(TILE)
        self.canvas.delete(TRANSITIONS)
        
        self.text_size = self.canvas.winfo_width() // (self.num_states * 6)
        
        # Draw all transitions as arcs, with costs
        for c, state in enumerate(self.state_list):
            if self.current_state.graph[state] is not None:
                for to_state in self.current_state.graph[state]:
                    c2 = self.state_list.index(to_state)
                    self.draw_arc_between(c, c2, self.current_state.graph[state][to_state])

        # Draw all the states as tiles on the top
        for c, state in enumerate(self.state_list):
            box_coords = self.calculate_box_coords(0,c)
            self.canvas.create_rectangle(*box_coords, fill= COLORS[TILE], tag=TILE)
            center_coords = self.calculate_center_coords(0,c)
            self.canvas.create_text(*center_coords, text=state, fill= COLORS[TEXT], anchor=S,
                                    font = ('Times New Roman', self.text_size, 'bold' ), tag=TEXT)
            self.canvas.create_text(*center_coords, text="H: " + str(self.current_state.heuristics[state]), fill= COLORS[TEXT], anchor=N,
                                    font = ('Times New Roman', self.text_size, 'bold' ), tag=TEXT)
            
        


    def click_canvas_to_action(self, event) -> GraphAction:
        h = self.canvas.winfo_height() # Get current height of canvas
        row = event.y // (h //  (self.num_states//2))
        if row > 0:
            return None
        w = self.canvas.winfo_width() # Get current width of canvas
        col = event.x // (w //  self.num_states)
        return GraphAction(self.state_list[col])


if __name__ == "__main__":
    if len(argv) > 1:
        file_path = argv[1]
    else: 
        initroot = Tk()
        initroot.withdraw()
        file_path = filedialog.askopenfilename(title = "Open Graph File",initialdir = getcwd(), filetypes=[("Graph", ".graph"), ("Text", ".txt")])
        initroot.destroy()
    initial_state = GraphState.readFromFile(file_path)
    gui = Graph_GUI(initial_state,algorithm_names=ALGORITHMS.keys(), strategy_names=STRATEGIES.keys(), heuristics=GRAPH_HEURISTICS)
    controller = Search_GUI_Controller(gui, initial_state, GRAPH_HEURISTICS)
    gui.mainloop()