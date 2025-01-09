import tkinter
import numpy as np
import math

m = tkinter.Tk()
m.resizable(False, False)

cw, ch = 1280, 720

w = tkinter.Canvas(m, width=cw, height=ch)
w.create_rectangle(0, 0, cw, ch, fill="#faa", outline="#faa")

start_grid = (cw / 2 - (ch * 7 / 12))
grid_width =  ch / 6

board_yellow_qubits = np.zeros((7, 6))
board_red_qubits = np.zeros((7, 6))

red_turn = True

board = np.zeros((7,6))

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
    
    for i in range(6):
        if board[col][5 - i] == 0.:
            board[col][5 - i] = 1 if red_turn else 2
            offx, offy = get_pos(col, 5 - i)
            w.create_oval(offx, offy, offx + grid_width - 10, offy + grid_width - 10, fill="#f00" if red_turn else "#ff0", outline="#faa")
            red_turn = not red_turn
            check_win()
            break
        if i == 5:
            print("no space")

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
            


w.pack()
m.bind("<Button-1>", on_place_click)
m.mainloop()