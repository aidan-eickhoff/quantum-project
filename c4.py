import tkinter
import numpy as np
import random
from rotation_input import Rotation_input
from input_panel import Input_panel

class Turn:
    def __init__(self, move_number, color):
        self.move_number = move_number
        self.color = color
        self.type = ""

class SuperTurn(Turn):
    def __init__(self, move_number, color, distribution=np.zeros(7)):
        super().__init__(move_number, color)
        self.distribution = distribution # -> array len 7 of floats
        self.type = "super"

class EntangleTurn(Turn):
    def __init__(self, move_number, color, mapping, linked_turn):
        super().__init__(move_number, color)
        self.mapping = mapping # -> array len 7 of ints
        self.linked_turn = linked_turn
        self.type = "entanglement"

class BoardState():
    def __init__(self):
        self.board = np.zeros((7, 6))
        self.moves = []
        self.last_collapsed_move = 0
        self.total_move_number = 0
        self.red_turn = True

    # add a classical piece to a column in a board_state (self.board if None is supplied)
    def add_to_col(self, col: int, is_red:bool, curr_board: np.ndarray | None = None) -> np.ndarray:
        if curr_board is None:
            curr_board = self.board
        for row in range(6):
            if curr_board[col][5 - row] == 0.:
                # 1 in array represents red, 2 represents yellow
                curr_board[col][5 - row] = 1 if is_red else 2
                self.check_win()
                break
            if row == 5:
                print("no space")
        return curr_board
    

    # check for a winning move on the current board
    def check_win(self):
        for col in range(0, 7):
            for row in range(0, 6):
                if row < 3 and self.board[col][row] == self.board[col][row + 1] == self.board[col][row + 2] == self.board[col][row + 3] != 0:
                    print("winner " + ("red" if self.board[col][row] == 1 else "yellow"))
                if col < 4 and self.board[col][row] == self.board[col + 1][row] == self.board[col + 2][row] == self.board[col + 3][row] != 0:
                    print("winner " + ("red" if self.board[col][row] == 1 else "yellow"))
                if row < 3 and col < 4 and self.board[col][row] == self.board[col + 1][row + 1] == self.board[col + 2][row + 2] == self.board[col + 3][row + 3] != 0:
                    print("winner " + ("red" if self.board[col][row] == 1 else "yellow"))
                if row < 3 and col > 2 and self.board[col][row] == self.board[col - 1][row + 1] == self.board[col - 2][row + 2] == self.board[col - 3][row + 3] != 0:
                    print("winner " + ("red" if self.board[col][row] == 1 else "yellow"))


    # called to collapse the board up to a target turn -- returns the updated board
    def collapse_event(self, target_turn: int|None = None) -> np.ndarray:
        if target_turn is None:
            target_turn = len(self.moves)
        if target_turn <= self.last_collapsed_move:
            print("Error, collapsing moves which are already collapsed")
            return
        new_board = self.collapse_moves(self.moves[self.last_collapsed_move:target_turn])
        self.last_collapsed_move = target_turn
        return new_board


    # takes a list of moves and a starting board state -- if starting state is none use the board 
    # calculates the resulting collapsed state. If None supplied as starting state, auto-update game state
    def collapse_moves(self, moves: list, starting_board: np.ndarray|None = None) -> np.ndarray:
        # starting state
        curr_board = starting_board if starting_board is not None else self.board
        # previous columns 
        prev_move_cols = []
        # pass through all the moves which need to be collapsed
        for move in moves:
            match move.type:
                # superposition move logic
                case "super":
                    rand = random.random()
                    count = move.distribution[0]
                    for col in range(0, 7):
                        # if true, we have decided randomly on a collapsed superposition, and we save it
                        if rand < count:
                            prev_move_cols.append(col)
                            curr_board = self.add_to_col(col, move.color, curr_board=curr_board)
                            break
                        if col == 7:
                            # SHOULD NEVER GET HERE IF PROBABILITIES ARE 1
                            return 0
                        count += move.distribution[col + 1]
                # entanglement move logic
                case "entanglement":
                    entangled_col = move.mapping[prev_move_cols[move.linked_turn - self.last_collapsed_move]]
                    curr_board = self.add_to_col(entangled_col, move.color, curr_board=curr_board)
                case _:
                    print("ERROR")
        return curr_board
        

    def add_move(self, dist: np.ndarray, is_entanglement_move: bool, target_turn: int = 0):
        if not is_entanglement_move:
            self.moves.append(SuperTurn(move_number=self.total_move_number, distribution=dist, color=self.red_turn))
        else:
            if target_turn < self.last_collapsed_move or self.moves[target_turn].type != "super":
                print("Not a valid target turn")
                return
            self.moves.append(EntangleTurn(move_number=self.total_move_number, mapping=dist, linked_turn=target_turn, color=self.red_turn))
        self.red_turn = not self.red_turn


class tkinterHandler():
    def __init__(self):
        self.main_window = tkinter.Tk()
        # Tkinter interactable widgets
        self.input_move_type = tkinter.IntVar()
        # self.move_type = tkinter.Checkbutton(self.main_window, text="Entanglement move", variable=self.input_move_type, onvalue=1, offvalue=0)
        # self.input_text = tkinter.Text(self.main_window, height = 1, width = 40) 
        # self.column_input_container = tkinter.Frame()
        # self.column_inputs = create_amplitudes_inputs(self.column_input_container)
        # self.target_turn_number = tkinter.Text(self.main_window, height = 1, width = 4) 
        # self.submit_button = tkinter.Button(self.main_window, text='Input move', command=self.add_move)

        # board size & place information
        self.board_width, self.board_height = 1280, 400
        self.start_board_x_pos = (self.board_width / 2 - (self.board_height * 7 / 12))
        self.grid_width =  self.board_height / 6
        # create drawable canvas
        self.canvas = tkinter.Canvas(self.main_window, width=self.board_width, height=self.board_height)
        self.canvas.create_rectangle(0, 0, self.board_width, self.board_height, fill="#faa", outline="#faa")
        for col in range(0, 7):
            for row in range(0, 6):
                self.fill_piece(col, row, fill="#fff")

        self.canvas.pack()
        self.input_panel = Input_panel(self.main_window, self.add_move) #constructor performs .pack()
        # self.move_type.pack()
        # self.column_input_container.pack()
        # self.input_text.pack() 
        # self.target_turn_number.pack()
        # self.submit_button.pack()

        self.main_window.bind("a", self.collapse)

        self.board_state: BoardState = BoardState()


    def show_window(self):
        self.main_window.mainloop()


    def get_pos(self, col: int, row: int) -> tuple[int, int]:
        return (self.start_board_x_pos + col * self.grid_width + 5, row * self.grid_width + 5)


    def fill_piece(self, col: int, row: int, fill):
        offx, offy = self.get_pos(col, row)
        self.canvas.create_oval(offx, offy, offx + self.grid_width - 10, offy + self.grid_width - 10, fill=fill, outline="#faa")


    def add_move(self) -> BoardState:
        text_input = self.input_panel.entanglement_input.get(1.0, "end-1c") 
        match self.input_move_type.get():
            # superposition case
            case 0:
                # array = np.array(list(map(float, text_input.split(','))))
                # array *= 1 / np.sum(array)
                self.board_state.add_move(probs, False)
            # entanglement case
            case 1:
                target_turn = int(self.target_turn_number.get(1.0, "end-1c"))
                array = np.array(list(map(int, text_input.split(','))))
                self.board_state.add_move(array, True, target_turn=target_turn)

    def collapse(self, event):
        new_board = self.board_state.collapse_event()
        for col in range(0, 7):
            for row in range(0, 6):
                if new_board[col][row] != 0:
                    self.fill_piece(col, row, "#f00" if (new_board[col][row] == 1) else "#ff0")
        self.board_state.board = new_board



tkinter_handler = tkinterHandler()
tkinter_handler.show_window()