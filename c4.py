import tkinter
import numpy as np
import math
import random
from coords_input import create_coords_inputs

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

m = tkinter.Tk()

#getting screen width and height of display
width= m.winfo_screenwidth() 
height= m.winfo_screenheight()
#setting tkinter window size
m.geometry("%dx%d" % (width, height))
m.title("Qonnect 4")
# m.resizable(False, False)

cw, ch = 1280, 600

w = tkinter.Canvas(m, width=cw, height=ch)
w.create_rectangle(0, 0, width, height, fill="#faa", outline="#faa")

input_move_type = tkinter.IntVar()
move_type = tkinter.Checkbutton(m, text="Entanglement move", variable=input_move_type, onvalue=1, offvalue=0)
coord_input_frame = tkinter.Frame()
coord_inputs = create_coords_inputs(coord_input_frame)
input_text = tkinter.Text(m, height = 1, width = 40) 
target_turn_number = tkinter.Text(m, height = 1, width = 4) 

start_grid = (cw / 2 - (ch * 7 / 12))
grid_width =  ch / 6

board = np.zeros((7, 6))
moves = []
start_queue = 0
total_move_number = 0

red_turn = True

def collapse_moves(moves: list) -> list:
    global board, start_queue
    curr_board_state = board
    move_cols = []
    for move in moves:
        match move.type:
            case "super":
                rand = random.random()
                count = move.distribution[0]
                for col in range(0, 7):
                    if rand < count:
                        move_cols.append(col)
                        curr_board_state = add_to_col(curr_board_state, col, is_red=move.color)
                        break
                    # THIS SHOULD NEVER GET CALLED IF PROBABILITIES ARE 1
                    if col == 7:
                        return 0
                    count += move.distribution[col + 1]
            case "entanglement":
                curr_board_state = add_to_col(curr_board_state, move.mapping[move_cols[move.linked_turn - start_queue]], is_red=move.color)
            case _:
                print("ERROR")

def collapse(event, target_turn: int|None = None) -> None:
    global start_queue, moves
    if target_turn is None:
        target_turn = len(moves)
    collapse_moves(moves[start_queue:target_turn])
    start_queue=target_turn



def add_to_col(board_state: np.ndarray, col: int, is_red=True) -> np.ndarray:
    for i in range(6):
        if board_state[col][5 - i] == 0.:
            board_state[col][5 - i] = 1 if red_turn else 2
            offx, offy = get_pos(col, 5 - i)
            w.create_oval(offx, offy, offx + grid_width - 10, offy + grid_width - 10, fill="#f00" if is_red else "#ff0", outline="#faa")
            check_win()
            break
        if i == 5:
            print("no space")
    return board_state

def get_pos(col, row):
    return (start_grid + col * grid_width + 5, 0 + row * grid_width + 5)

for i in range(0, 7):
    for j in range(0, 6):
        offx, offy = get_pos(i, j)
        w.create_oval(offx, offy, offx + grid_width - 10, offy + grid_width - 10, fill="#fff", outline="#faa")

def on_place_click(event):
    global red_turn, start_grid, get_pos
    col = math.floor((event.x - start_grid) / grid_width)

    if col < 0 or col > 7:
        return
    board = add_to_col(board, col, is_red=red_turn)
    red_turn = not red_turn

def check_win():
    global board
    for col in range(0, 7):
        for row in range(0, 6):
            if row < 3 and board[col][row] == board[col][row + 1] == board[col][row + 2] == board[col][row + 3] != 0:
                print("winner " + ("red" if board[col][row] == 1 else "yellow"))
            if col < 4 and board[col][row] == board[col + 1][row] == board[col + 2][row] == board[col + 3][row] != 0:
                print("winner " + ("red" if board[col][row] == 1 else "yellow"))
            if row < 3 and col < 4 and board[col][row] == board[col + 1][row + 1] == board[col + 2][row + 2] == board[col + 3][row + 3] != 0:
                print("winner " + ("red" if board[col][row] == 1 else "yellow"))
            if row < 3 and col > 2 and board[col][row] == board[col - 1][row + 1] == board[col - 2][row + 2] == board[col - 3][row + 3] != 0:
                print("winner " + ("red" if board[col][row] == 1 else "yellow"))
            

def add_move(distribution: np.ndarray =np.zeros(7), mapping: np.ndarray =np.zeros(7), target_turn=0):
    global moves, total_move_number, red_turn, input_move_type
    text_input = input_text.get(1.0, "end-1c") 
    match input_move_type.get():
        case 0:
            array = np.array(list(map(float, text_input.split(','))))
            if len(array) < 7:
                np.pad(array, 7 - len(array))
            array *= 1 / np.sum(array)
            print(array)
            moves.append(SuperTurn(move_number=total_move_number, distribution=array, color=red_turn))
            red_turn = not red_turn
        case 1:
            target_turn = int(target_turn_number.get(1.0, "end-1c"))
            if target_turn < start_queue or moves[target_turn].type != "super":
                print("Not a valid target turn")
                return
            array = np.array(list(map(int, text_input.split(','))))
            if len(array) < 7:
                np.pad(array, 7 - len(array))
            moves.append(EntangleTurn(move_number=total_move_number, mapping=array, linked_turn=target_turn, color=red_turn))
            red_turn = not red_turn

    target_turn += 1
    print(moves)

submit_button = tkinter.Button(m, text='Input move', command=add_move)


w.pack()

move_type.pack()
coord_input_frame.pack()
input_text.pack() 
target_turn_number.pack()
submit_button.pack()
  
m.bind("a", collapse)

m.mainloop()