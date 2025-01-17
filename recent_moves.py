import tkinter
# requires gui package as main python file is outside of package
from gui.rotation_input import Rotation_input
from gui.CY_input import CY_input

class Recent_moves_list():
    def __init__(self, parent):
        self.container = tkinter.Frame(parent, borderwidth=2, relief=tkinter.RIDGE)
        self.moves = []
        self.moves_var = tkinter.StringVar(value=self.moves)

        self.list = tkinter.Listbox(self.container, listvariable=self.moves_var)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.list.grid(row=0,column=0, sticky = 'nsew')

    def add_move(self, move):
        move_num = str(len(self.moves) + 1)
        self.moves.append(move_num + ". " + str(move))
        self.moves_var.set(list(reversed(self.moves)))
