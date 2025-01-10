import tkinter
import numpy as np
import random

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
        self.num_shots = 4_096

    # add a classical piece to a column in a board_state (self.board if None is supplied)
    def add_to_col(self, col: int, is_red:bool, curr_board: np.ndarray) -> np.ndarray:
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
    

    def estimate_evs(self) -> tuple[np.ndarray, np.ndarray]:
        red_ev, yellow_ev = np.zeros((7, 6)), np.zeros((7, 6))
        for i in range(0, self.num_shots):
            board = self.collapse_moves(self.moves[self.last_collapsed_move:], starting_board=np.array(self.board))
            red_ev += (board % 2) / self.num_shots
            yellow_ev += np.floor(board / 2) / self.num_shots
        return (red_ev, yellow_ev)
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
                    try:
                        entangled_col = move.mapping[prev_move_cols[move.linked_turn - self.last_collapsed_move]]
                        prev_move_cols.append(0)
                    except:
                        print("Entanglement debug")
                        print("linked turn" + str(move.linked_turn))
                        print("last collapsed " + str(self.last_collapsed_move))
                        print("move mapping " + str(move.mapping))
                        print("prev move columns " + str(prev_move_cols))
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
        self.total_move_number += 1


class tkinterHandler():
    def __init__(self):
        self.main_window = tkinter.Tk()
        # Tkinter interactable widgets
        self.input_move_type = tkinter.IntVar()
        self.move_type = tkinter.Checkbutton(self.main_window, text="Entanglement move", variable=self.input_move_type, onvalue=1, offvalue=0)
        self.input_text = tkinter.Text(self.main_window, height = 1, width = 40) 
        self.target_turn_number = tkinter.Text(self.main_window, height = 1, width = 4) 
        self.submit_button = tkinter.Button(self.main_window, text='Input move', command=self.add_move)
        self.delete_button = tkinter.Button(self.main_window, text='remove last', command=self.removelast)
        self.change_player = tkinter.Button(self.main_window, text='change player', command=self.changeplayer)

        # board size & place information
        self.board_width, self.board_height = 1280, 720
        self.start_board_x_pos = (self.board_width / 2 - (self.board_height * 7 / 12))
        self.grid_width =  self.board_height / 6
        # create drawable canvas
        self.canvas = tkinter.Canvas(self.main_window, width=self.board_width, height=self.board_height)
        self.canvas.create_rectangle(0, 0, self.board_width, self.board_height, fill="#faa", outline="#faa")
        for col in range(0, 7):
            for row in range(0, 6):
                self.fill_piece(col, row, fill="#fff")

        self.canvas.pack()
        self.move_type.pack()
        self.input_text.pack() 
        self.target_turn_number.pack()
        self.submit_button.pack()
        self.delete_button.pack()
        self.change_player.pack()
        self.main_window.bind("a", self.collapse)

        self.board_state: BoardState = BoardState()

    def removelast(self):
        self.board_state.moves.pop()
        self.board_state.total_move_number -= 1
        self.update_evs()
        print(self.board_state.moves)

    def changeplayer(self):
        self.board_state.red_turn = not self.board_state.red_turn
        print("now player " + ("red " if self.board_state.red_turn else "yellow"))

    def show_window(self):
        self.main_window.mainloop()


    def get_pos(self, col: int, row: int) -> tuple[int, int]:
        return (self.start_board_x_pos + col * self.grid_width + 5, row * self.grid_width + 5)


    def fill_piece(self, col: int, row: int, fill):
        offx, offy = self.get_pos(col, row)
        self.canvas.create_oval(offx, offy, offx + self.grid_width - 10, offy + self.grid_width - 10, fill=fill, outline="#faa")


    def add_move(self) -> BoardState:
        text_input = self.input_text.get(1.0, "end-1c") 
        match self.input_move_type.get():
            # superposition case
            case 0:
                array = np.array(list(map(float, text_input.split(','))))
                array /= np.sum(array)
                if len(array) > 7:
                    print("illegal")
                    return
                self.board_state.add_move(array, False)
            # entanglement case
            case 1:
                target_turn = int(self.target_turn_number.get(1.0, "end-1c"))
                array = np.array(list(map(int, text_input.split(','))))
                if len(array) > 7 or len(array[np.where(array >= 7)]) != 0:
                    print("illegal")
                    return
                self.board_state.add_move(array, True, target_turn=target_turn)
        print(self.board_state.total_move_number - 1)
        self.update_evs()

    def update_evs(self):
        red_ev, yellow_ev = self.board_state.estimate_evs()
        for col in range(0, 7):
            for row in range(0, 6):
                self.fill_piece(col, row, fill="#fff")
                if 0. < (red_ev[col][row] + yellow_ev[col][row]) and red_ev[col][row] + 1e-3 < 1 and yellow_ev[col][row] + 1e-3 < 1:
                    redangle = red_ev[col][row] * 359 # 359 looks better than 360
                    yellow_angle = yellow_ev[col][row] * 359
                    # yellow_final = redangle + yellow_angle
                    offx, offy = self.get_pos(col, row)
                    self.canvas.create_arc(offx, offy, offx + self.grid_width - 10, offy + self.grid_width - 10, fill="#f00", outline="", start=0,        extent=redangle,     style=tkinter.PIESLICE)
                    self.canvas.create_arc(offx, offy, offx + self.grid_width - 10, offy + self.grid_width - 10, fill="#ff0", outline="", start=redangle, extent=yellow_angle, style=tkinter.PIESLICE)
                elif red_ev[col][row] + 1e-3 >= 1.:
                    self.fill_piece(col, row, fill="#f00")
                elif yellow_ev[col][row] + 1e-3 >= 1.:
                    self.fill_piece(col, row, fill="#ff0")


    def collapse(self, event):
        new_board = self.board_state.collapse_event()
        if new_board is None:
            return
        for col in range(0, 7):
            for row in range(0, 6):
                color = "#f00" if (new_board[col][row] == 1) else ("#ff0" if new_board[col][row] == 2 else "#fff")
                self.fill_piece(col, row, color)

        self.board_state.board = new_board
        print(self.board_state.last_collapsed_move)




tkinter_handler = tkinterHandler()
tkinter_handler.show_window()