"""
GUI for your solutions to Lab 1, Part 2.
Usage:
    python lab1_part1_gui.py [APP] [INITIAL_STATE_FILE]
    APP can be "roomba" or "slidepuzzle"
    INITIAL_STATE_FILE is a path to a text file that will be parsed
    by either RoombaMultiRouteState or SlidePuzzleState
"""

from sys import argv
import time
from tkinter import *
from lab1_solutions import RandWalk, DFS, BFS, UCS
from lab1_solutions import GreedyBest, AStar
from lab1_part2_heuristics import *
from roomba_multi_state import RoombaMultiRouteState, FLOOR, CARPET, WALL, GOAL

from slidepuzzle_state import SlidePuzzleState

WIDTH = 500

TILE, EMPTY, PATH, TEXT = 'tile', 'empty', 'path', 'text'
AGENT, START, PATH, SEEN = 'agent', 'start', 'path', 'seen'

COLORS = {FLOOR : 'pale green', CARPET : 'RoyalBlue1', WALL : 'gray25', GOAL : 'saddle brown',
          AGENT:"orange red", START: 'IndianRed1', PATH: 'IndianRed1', SEEN: 'black',
          TILE : 'gray', EMPTY : 'white', PATH: 'IndianRed1', TEXT: 'black'}

UNINFORMED_ALGORITHMS = {"RandWalk" : RandWalk, "DFS" : DFS, "BFS" : BFS, "UCS" : UCS}
INFORMED_ALGORITHMS =  {"GreedyBest" : GreedyBest, "A*" : AStar}
ALGORITHMS =  {**UNINFORMED_ALGORITHMS, **INFORMED_ALGORITHMS} # shallow combination copy

ROOMBA_HEURISTICS = {"Zero" : zero_heuristic, "Manhattan (one goal)" : roomba_manhattan_onegoal}
ROOMBA_HEURISTICS.update(all_multi_heuristics)
PUZZLE_HEURISTICS =  {"Zero" : zero_heuristic, "Hamming" : slidepuzzle_hamming, "Manhattan" : slidepuzzle_manhattan}



STEP_TIME_OPTIONS = (0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09,
                    0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 2.0, 5.0)

CUTOFF_OPTIONS = tuple( ['INF'] + list(range(1,10)) + list(range(10,101,10)))

INITIAL_WAITING = 0
SEARCHING_RUNNING = 1
SEARCHING_PAUSED = 2
SEARCHING_STEP = 3
FINISHED_SUCCESS = 4
FINISHED_FAILURE = 5
VALID_STATUSES = [INITIAL_WAITING, SEARCHING_RUNNING, SEARCHING_PAUSED, SEARCHING_STEP,
                    FINISHED_SUCCESS, FINISHED_FAILURE]

STATUS_TEXT = {  INITIAL_WAITING: "Pick an algorithm and Run or Step.",
                SEARCHING_RUNNING:"{} is running... (Pause or Step)",
                SEARCHING_PAUSED: "{} is paused. (Run or Step)",
                SEARCHING_STEP:   "{} is paused. (Run or Step).",
                FINISHED_SUCCESS: "{} completed succesfully!",
                FINISHED_FAILURE: "{} terminated unsuccessfully."}

class Lab1GUI_IS:
    def __init__(self, master, initial_state, canvas_height, canvas_width):
        self.master = master

        self.initial_state = initial_state
        self.current_state = initial_state

        self.canvas = Canvas(master, height=canvas_height, width=canvas_width, bg='white')

        self.canvas.grid(row = 0, columnspan = 4) #pack(fill=tk.BOTH, expand=True)
        self.canvas.bind('<Configure>', lambda *args : self.draw_background() or self.draw_path_to_state() )

        algorithm_frame = Frame(master)
        algorithm_frame.grid(row = 1, column = 0, sticky = NW)

        self.algorithm_listbox = Listbox(algorithm_frame, selectmode = BROWSE, height = len(ALGORITHMS), exportselection = 0)
        self.algorithm_listbox.grid(row= 0, column =0, sticky = NW)
        for item in ALGORITHMS.keys():
            self.algorithm_listbox.insert(END, item)
        self.algorithm_listbox.select_set(0) # This only sets focus on the first item.
        self.algorithm_listbox.event_generate("<<ListboxSelect>>")

        self.current_algorithm = self.get_alg_selection()

        self.avoid_backtrack_state = IntVar()
        self.avoid_backtrack_checkbox = Checkbutton(algorithm_frame, text='Avoid backtrack?', variable=self.avoid_backtrack_state)
        self.avoid_backtrack_checkbox.grid(row= 1, column = 0, sticky = NW)

        self.filtering_state = IntVar()
        self.filtering_checkbox = Checkbutton(algorithm_frame, text='\'Extended\' filter?', variable=self.filtering_state)
        self.filtering_checkbox.grid(row= 2, column = 0, sticky = NW)

        cutoff_frame = Frame(algorithm_frame)
        cutoff_frame.grid(row = 3, column = 0, sticky = NW)
        self.cutoff_label = Label(cutoff_frame, text="Cutoff")
        self.cutoff_label.grid(row = 0, column = 0, sticky = NW)

        self.cutoff_spinbox = Spinbox(cutoff_frame,
        values=CUTOFF_OPTIONS, width = 5, wrap = True)
        self.cutoff_spinbox.grid(row= 0, column = 1, sticky = NW)
        while(self.cutoff_spinbox.get() != "INF") :
            self.cutoff_spinbox.invoke('buttonup')

        heuristics_frame = Frame(master)
        heuristics_frame.grid(row = 1, column = 1, sticky = NW)
        heuristics_label = Label(heuristics_frame, text="Heuristic:")
        heuristics_label.grid(row = 0, column = 0, sticky = NW)
        # set self.heuristic_dict in init of subclass
        if not hasattr(self, 'heuristic_dict'):
            self.heuristic_dict = {}
        self.heuristic_listbox = Listbox(heuristics_frame, selectmode = BROWSE, height = len(self.heuristic_dict), exportselection = 0)
        self.heuristic_listbox.grid(row= 1, column =0, sticky = NW)
        for item in self.heuristic_dict.keys():
            self.heuristic_listbox.insert(END, item)
        self.heuristic_listbox.select_set(0) # This only sets focus on the first item.
        self.heuristic_listbox.event_generate("<<ListboxSelect>>")

        self.current_heuristic = self.get_heuristic_selection()


        run_options_frame = Frame(master)
        run_options_frame.grid(row = 1, column = 2, sticky = NW)


        self.reset_button = Button(run_options_frame, text="Reset",
                            command= self.reset_to_initial_waiting, width = 10)
        self.reset_button.grid(row= 0, column = 0, sticky = NW)


        self.run_pause_button = Button(run_options_frame, text="Run",
                            command= self.toggle_run_pause, width = 10)
        self.run_pause_button.grid(row= 1, column = 0, sticky = NW)

        self.step_button = Button(run_options_frame, text="Step",
                            command=self.step,width = 10)
        self.step_button.grid(row= 2, column = 0, sticky = NW)

        self.visualize_extends_state = IntVar()
        self.visualize_extends_state.set(1)
        self.visualize_extends_checkbox = Checkbutton(run_options_frame, text='Visualize each step?', variable=self.visualize_extends_state)
        self.visualize_extends_checkbox.grid(row= 3, column = 0, sticky = NW)

        self.print_status_state = IntVar()
        self.print_status_state.set(1)
        self.print_status_checkbox = Checkbutton(run_options_frame, text='Print progress?', variable=self.print_status_state)
        self.print_status_checkbox.grid(row= 4, column = 0, sticky = NW)


        step_time_spinbox_frame = Frame(run_options_frame)
        step_time_spinbox_frame.grid(row = 5, column = 0,sticky = NW)

        self.step_time_label = Label(step_time_spinbox_frame, text = "Step time: ")
        self.step_time_label.grid(row= 0, column = 0, sticky = NW)

        self.step_time_spinbox = Spinbox(step_time_spinbox_frame,
        values=STEP_TIME_OPTIONS, format="%3.2f", width = 4)
        self.step_time_spinbox.grid(row= 0, column = 1, sticky = NW)
        while(self.step_time_spinbox.get() != "0.1") :
            self.step_time_spinbox.invoke('buttonup')


        status_output_frame = Frame(master)
        status_output_frame.grid(row = 1, column = 3,sticky = NW)

        self.status = None
        self.status_text = StringVar()
        self.status_label = Label(status_output_frame, textvariable = self.status_text, width = "30")
        self.status_label.grid(row= 0, sticky = NW)

        self.last_action_text = StringVar()
        self.last_action_label = Label(status_output_frame, textvariable = self.last_action_text)
        self.last_action_label.grid(row= 1,sticky = NW)

        self.counter_dict = {'num_enqueues':0, 'num_extends':0}
        self.counter_text_1 = StringVar()
        self.counter_label_1 = Label(status_output_frame, textvariable = self.counter_text_1)
        self.counter_label_1.grid(row= 2,sticky = NW)

        self.counter_text_2 = StringVar()
        self.counter_label_2 = Label(status_output_frame, textvariable = self.counter_text_2)
        self.counter_label_2.grid(row= 3,sticky = NW)

        self.current_path_text_1 = StringVar()
        self.current_path_label_1 = Label(status_output_frame, textvariable = self.current_path_text_1)
        self.current_path_label_1.grid(row= 4,sticky = NW)

        self.current_path_text_2 = StringVar()
        self.current_path_label_2 = Label(status_output_frame, textvariable = self.current_path_text_2)
        self.current_path_label_2.grid(row= 5,sticky = NW)

        self.heuristic_text = StringVar()
        self.heuristic_label = Label(status_output_frame, textvariable = self.heuristic_text)
        self.heuristic_label.grid(row= 6,sticky = NW)


        path_print_frame = Frame(status_output_frame)
        path_print_frame.grid(row = 7, column = 0,sticky = NW)

        self.print_path_states_button = Button(path_print_frame, text="Print Path Sts.",
                            command=self.print_path_states,width = 15)
        self.print_path_states_button.grid(row= 0, column = 0, sticky = NW)
        self.print_path_actions_button = Button(path_print_frame, text="Print Path Act.",
                            command=self.print_path_actions,width = 15)
        self.print_path_actions_button.grid(row= 0, column = 1, sticky = NW)

        ## Add label for heuristics

        self.update_status_and_ui(INITIAL_WAITING)


    def update_status_and_ui(self, newstatus = INITIAL_WAITING):
        if newstatus == self.status: # No change?
            return

        assert newstatus in VALID_STATUSES

        self.status = newstatus
        self.status_text.set(STATUS_TEXT[self.status].format(self.current_algorithm))

        if newstatus == INITIAL_WAITING :
            self.reset_button['state'] = DISABLED
            self.filtering_checkbox['state'] = NORMAL
            self.avoid_backtrack_checkbox['state'] = NORMAL
            self.cutoff_spinbox['state'] = NORMAL
            self.step_button['state'] = NORMAL
            self.run_pause_button['state'] = NORMAL
            # self.print_path_actions_button['state'] = DISABLED
            # self.print_path_states_button['state'] = DISABLED

            self.run_pause_button['text'] = 'Run'


        elif newstatus in (SEARCHING_RUNNING,
                            SEARCHING_PAUSED, SEARCHING_STEP):
            self.reset_button['state'] = NORMAL
            self.filtering_checkbox['state'] = DISABLED
            self.avoid_backtrack_checkbox['state'] = DISABLED
            self.cutoff_spinbox['state'] = DISABLED
            self.step_button['state'] = NORMAL
            self.run_pause_button['state'] = NORMAL

            if newstatus == SEARCHING_RUNNING:
                self.run_pause_button['text'] = 'Pause'
            elif newstatus == SEARCHING_PAUSED: # moving away == starting searching
                self.run_pause_button['text'] = 'Run'
            elif newstatus == SEARCHING_STEP: # moving away == starting searching
                self.run_pause_button['text'] = 'Run'
                self.visualize_extends_state.set(1)
                self.print_status_state.set(1)


        elif newstatus in (FINISHED_FAILURE, FINISHED_SUCCESS):
            self.reset_button['state'] = NORMAL
            self.filtering_checkbox['state'] = DISABLED
            self.avoid_backtrack_checkbox['state'] = DISABLED
            self.cutoff_spinbox['state'] = DISABLED
            self.step_button['state'] = DISABLED
            self.run_pause_button['state'] = DISABLED
            # if newstatus == FINISHED_SUCCESS:
            #     self.print_path_states_button['state'] = NORMAL
            #     self.print_path_actions_button['state'] = NORMAL


    def print_path_states(self) :
        print("Path states: (length {})".format(self.current_state.get_path_length()))
        for n, state in enumerate(self.current_state.get_path()):
            if n > 0:
                print('{}: {}'.format(str(n), state.describe_previous_action()))
            print(str(state))

    def print_path_actions(self) :
        print("Path actions: (length {})".format(self.current_state.get_path_length()))
        for n, state in enumerate(self.current_state.get_path()):
            if n > 0:
                print('{}: {}'.format(str(n), state.describe_previous_action()))

    def get_alg_selection(self) :
        return self.algorithm_listbox.get(self.algorithm_listbox.curselection()[0])

    def get_heuristic_selection(self) :
        return self.heuristic_listbox.get(self.heuristic_listbox.curselection()[0])


    def start_search(self, event = None, initial_status = SEARCHING_RUNNING):
        self.current_algorithm = self.get_alg_selection()
        self.current_heuristic = self.get_heuristic_selection()
        self.update_status_and_ui(initial_status)
        self.counter_dict = {'num_enqueues':0, 'num_extends':0} #reset counter

        search_alg = ALGORITHMS[self.get_alg_selection()]
        heuristic = self.heuristic_dict[self.get_heuristic_selection()]
        if search_alg in UNINFORMED_ALGORITHMS.values():
            final_state = search_alg(self.initial_state,
                                    state_callback_fn = self.alg_callback,
                                    avoid_backtrack = bool(self.avoid_backtrack_state.get()),
                                    filtering = bool(self.filtering_state.get()),
                                    cutoff = float(self.cutoff_spinbox.get()),
                                    counter = self.counter_dict)
        elif search_alg in INFORMED_ALGORITHMS.values():

            final_state = search_alg(self.initial_state,
                                    heuristic_fn = heuristic,
                                    state_callback_fn = self.alg_callback,
                                    avoid_backtrack = bool(self.avoid_backtrack_state.get()),
                                    filtering = bool(self.filtering_state.get()),
                                    cutoff = float(self.cutoff_spinbox.get()),
                                    counter = self.counter_dict)

        if self.status != INITIAL_WAITING : # if termination not due to reset
            if (final_state is None):
                self.update_status_and_ui(FINISHED_FAILURE)
            else:
                self.current_state = final_state
                self.visualize_state(final_state)
                self.update_text(final_state)
                self.update_status_and_ui(FINISHED_SUCCESS)

    def reset_to_initial_waiting(self, event = None) :
        self.current_state = self.initial_state
        self.draw_path_to_state()
        self.clear_seen_list()
        self.update_status_and_ui(INITIAL_WAITING)


    def toggle_run_pause(self, event = None):
        # self.paused = False
        # self.pause_continue_button['text'] = 'Pause'
        if self.status == INITIAL_WAITING:
            self.start_search(initial_status = SEARCHING_RUNNING)
        elif self.status == SEARCHING_PAUSED or self.status == SEARCHING_STEP :
            self.update_status_and_ui(SEARCHING_RUNNING)
        elif self.status == SEARCHING_RUNNING :
            self.update_status_and_ui(SEARCHING_PAUSED)

    def step(self):
        if self.status == INITIAL_WAITING :
            self.start_search(initial_status = SEARCHING_PAUSED)
        elif  self.status == SEARCHING_RUNNING or self.status == SEARCHING_PAUSED :
            self.update_status_and_ui(SEARCHING_STEP)



    def alg_callback(self, state):
        self.run_pause_button.update()
        self.step_button.update()
        self.reset_button.update()
        self.visualize_extends_checkbox.update()
        self.print_status_checkbox.update()

        while self.status == SEARCHING_PAUSED :
            time.sleep(.1)
            self.run_pause_button.update()
            self.step_button.update()
            self.reset_button.update()

        if self.status == SEARCHING_STEP:
            self.update_status_and_ui(SEARCHING_PAUSED)

        if self.print_status_state.get():
            self.update_text(state)
        if self.visualize_extends_state.get() :
            self.visualize_state(state)
        else:
            return (self.status == INITIAL_WAITING)

        if self.status == SEARCHING_RUNNING :
            time.sleep(float(self.step_time_spinbox.get()))

        return (self.status == INITIAL_WAITING)

    def update_text(self, state):

        self.last_action_text.set(
            'Last Action: {}'.format(state.describe_previous_action()))




        self.counter_text_1.set(
            'Extends: {}'.format(self.counter_dict['num_extends']))
        self.counter_text_2.set(
            'Enqueues: {}'.format(self.counter_dict['num_enqueues']))

        self.current_path_text_1.set(
            'Path Length: {}'.format(state.get_path_length()))

        self.current_path_text_2.set(
            'Path Cost: {}'.format(state.get_path_cost()))

        if self.current_algorithm in INFORMED_ALGORITHMS:
            h_val = self.heuristic_dict[self.current_heuristic](state)
            if self.current_algorithm == "A*":
                self.heuristic_text.set('{}: {:.2f}\n^Heur. + Path Cost^: {:.2f}'.format(self.current_heuristic, h_val, h_val + state.get_path_cost()))
            else:
                self.heuristic_text.set( '{}: {:.2f}'.format(self.current_heuristic, h_val) )
        else :
            self.heuristic_text.set('') # self.current_algorithm in UNINFORMED_ALGORITHMS:


        ### add display for heuristic values


    def visualize_state(self, state):
        self.current_state = state
        if self.filtering_state.get():
            self.update_draw_seen_list()
        self.draw_path_to_state()
        self.canvas.update()

    def update_draw_seen_list(self, event = None):
        raise NotImplementedError

    def clear_seen_list(self, event = None):
        raise NotImplementedError

    def draw_path_to_state(self, event = None):
        raise NotImplementedError

    def draw_background(self, event = None):
        raise NotImplementedError


class MazeMultiGUI(Lab1GUI_IS):
    def __init__(self, master, initial_state):
        master.title("Roomba Search Visualizer")
        self.maze_width = initial_state.get_width()
        self.maze_height = initial_state.get_height()
        self.heuristic_dict = ROOMBA_HEURISTICS
        self.text_size = WIDTH // self.maze_width // 2
        super().__init__(master, initial_state, canvas_height = self.maze_height*WIDTH / self.maze_width, canvas_width = WIDTH)

    def calculate_box_coords(self, r, c):
        w = self.canvas.winfo_width() # Get current width of canvas
        h = self.canvas.winfo_height() # Get current height of canvas
        x1 = w * c // self.maze_width
        y1 = h * r // self.maze_height
        x2 = w * (c + 1) // self.maze_width
        y2 = h * (r + 1) // self.maze_height
        return (x1, y1, x2, y2)

    def calculate_center_coords(self, r, c):
        w = self.canvas.winfo_width() # Get current width of canvas
        h = self.canvas.winfo_height() # Get current height of canvas
        x = int(w * (c + .5)) // self.maze_width
        y = int(h * (r + .5)) // self.maze_height
        return (x, y)

    def update_draw_seen_list(self, event = None):
        curr_r, curr_c = self.current_state.get_position()
        x1, y1, x2, y2 = self.calculate_box_coords(curr_r,curr_c)
        self.canvas.create_oval(x1, y1, x2, y2, fill= '', outline = COLORS['seen'], width = 2, dash = (4,4),tag='seen_list')

    def clear_seen_list(self, event = None):
        self.canvas.delete('seen_list')

    def draw_path_to_state(self, event = None):
        self.canvas.delete('path_line')
        self.canvas.delete('agent')
        self.canvas.delete('numbers')

        curr_r, curr_c = self.current_state.get_position()
        x1, y1, x2, y2 = self.calculate_box_coords(curr_r,curr_c)
        self.canvas.create_oval(x1, y1, x2, y2, fill= COLORS[AGENT], tag='agent')

        path = self.current_state.get_path()
        path_rc = [state.get_position() for state in path]
        path_coords = [self.calculate_center_coords(r,c)
                        for r,c in path_rc]
        if len(path_coords) > 1:
            self.canvas.create_line(path_coords, fill = COLORS[PATH], width = 3, tag='path_line', )

        # number the order of dirt cleaned
        dirt_count = 1
        dirt_seen = set()
        for (r,c), pos in  zip(path_rc, path_coords):
                if (self.initial_state.get_grid()[r][c] == GOAL
                    and pos not in dirt_seen
                    and self.current_state.get_grid()[r][c] != GOAL):
                    self.canvas.create_text(pos, fill = COLORS[TEXT], tag = 'numbers',
                        text = str(dirt_count), font = ('Times New Roman', self.text_size, 'bold' ))
                    dirt_count += 1
                    dirt_seen.add(pos)


    def draw_background(self, event = None):
        w = self.canvas.winfo_width() # Get current width of canvas
        h = self.canvas.winfo_height() # Get current height of canvas
        # Clear the background grid and terrain
        self.canvas.delete('grid_line')
        self.canvas.delete('terrain_block')

        # Creates all vertical lines
        for c in range(0, self.maze_width):
            x = w * c // self.maze_width
            self.canvas.create_line([(x, 0), (x, h)], tag='grid_line')

        # Creates all horizontal lines
        for r in range(0, self.maze_height):
            y = h * r // self.maze_height
            self.canvas.create_line([(0, y), (w, y)], tag='grid_line')

        # Draw terrain
        position = self.initial_state.get_position()
        maze = self.initial_state.get_grid()
        for r in range(0,self.maze_height):
            for c in range(0,self.maze_width):
                terrain = maze[r][c]
                x1, y1, x2, y2 = self.calculate_box_coords(r,c)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill= COLORS[terrain], tag='terrain_block')

        # Draw initial position
        r, c = position
        x1 = w * c // self.maze_width
        y1 = h * r // self.maze_height
        x2 = w * (c + 1) // self.maze_width
        y2 = h * (r + 1) // self.maze_height

        self.canvas.create_oval(x1, y1, x2, y2, fill= '', outline= COLORS[START], tag='start')



class SlidePuzzleGUI(Lab1GUI_IS):
    def __init__(self, master, initial_state):
        master.title("Slide Puzzle Search Visualizer")
        self.puzzle_dim = initial_state.size()
        self.puzzle_dim = initial_state.size()
        self.text_size = WIDTH // (self.puzzle_dim * 2)
        self.heuristic_dict = PUZZLE_HEURISTICS
        super().__init__(master, initial_state, canvas_height = WIDTH, canvas_width = WIDTH)

    def calculate_box_coords(self, r, c):
        w = self.canvas.winfo_width() # Get current width of canvas
        h = self.canvas.winfo_height() # Get current height of canvas
        x1 = w * c // self.puzzle_dim
        y1 = h * r // self.puzzle_dim
        x2 = w * (c + 1) // self.puzzle_dim
        y2 = h * (r + 1) // self.puzzle_dim
        return (x1, y1, x2, y2)

    def calculate_center_coords(self, r, c):
        w = self.canvas.winfo_width() # Get current width of canvas
        h = self.canvas.winfo_height() # Get current height of canvas
        x = int(w * (c + .5)) // self.puzzle_dim
        y = int(h * (r + .5)) // self.puzzle_dim
        return (x, y)

    def update_draw_seen_list(self, event = None):
        pass

    def clear_seen_list(self, event = None):
        pass

    def draw_path_to_state(self, event = None):
        self.canvas.delete('numbers')

        self.canvas.delete('empty_tile')
        self.canvas.delete('path_line')

        # draw number tiles and empty tile
        for r in range(0,self.puzzle_dim):
            for c in range(0,self.puzzle_dim):
                tile = self.current_state.tile_at(r,c)
                pos = self.calculate_center_coords(r,c)
                if tile != 0 :
                    self.canvas.create_text(pos, fill = COLORS[TEXT], tag = 'numbers',
                        text = str(tile), font = ('Times New Roman', self.text_size, 'bold' ))
                else :
                    x1, y1, x2, y2 = self.calculate_box_coords(r,c)
                    self.canvas.create_rectangle(x1+2, y1+2, x2-2, y2-2, fill= COLORS[EMPTY], tag='empty_tile')

        # draw path line
        path_coords = [self.calculate_center_coords(*state.get_empty_pos())
                        for state in self.current_state.get_path() ]
        if len(path_coords) > 1:
            self.canvas.create_line(path_coords, fill = COLORS[PATH], width = 4, tag='path_line')

    def draw_background(self, event = None):
        w = self.canvas.winfo_width() # Get current width of canvas
        h = self.canvas.winfo_height() # Get current height of canvas
        # Clear the background grid and tiles
        self.canvas.delete('grid_line')
        self.canvas.delete('tiles')

        # Draw all the "tiles" - really, background color
        self.canvas.create_rectangle(0, 0, w, h, fill= COLORS[TILE], tag='tiles')

        # Creates all vertical lines
        for c in range(0, self.puzzle_dim):
            x = w * c // self.puzzle_dim
            self.canvas.create_line([(x, 0), (x, h)], tag='grid_line', width = 3)

        # Creates all horizontal lines
        for r in range(0, self.puzzle_dim):
            y = h * r // self.puzzle_dim
            self.canvas.create_line([(0, y), (w, y)], tag='grid_line', width = 3)



if len(argv) < 3 :
    print("Usage:    python lab1_part1_gui.py [APP] [INITIAL_STATE_FILE]")
    print("          APP can be \"roomba\" or \"slidepuzzle\"")
    print("          INITIAL_STATE_FILE is a path to a text file")
    quit()
root = Tk()

if argv[1] == 'roomba':
    initial_state = RoombaMultiRouteState.readFromFile(argv[2])
    maze_gui = MazeMultiGUI(root, initial_state)

elif argv[1] == 'slidepuzzle':
    initial_state = SlidePuzzleState.readFromFile(argv[2])
    maze_gui = SlidePuzzleGUI(root, initial_state)
else :
    raise ValueError("First argument should be 'roomba' or 'slidepuzzle'")

root.mainloop()
