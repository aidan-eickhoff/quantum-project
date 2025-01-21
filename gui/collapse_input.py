import tkinter
import circuit_generation
import numpy as np

class Collapse_input():
    def __init__(self, parent):
        self.container = tkinter.Frame(parent)
        
        self.cell_x = tkinter.StringVar()
        self.cell_y = tkinter.StringVar()

        self.cell_label = tkinter.Label(self.container,text='Collapse move')
        self.cell_label.grid(row=0,column=0, columnspan=2)


        self.cell_label = tkinter.Label(self.container,text='Cell (X,Y)')
        self.cell_label.grid(row=1,column=0)
        self.cell_x_input = tkinter.Entry(self.container, textvariable=self.cell_x)
        self.cell_x_input.grid(row=2,column=0)
        self.cell_y_input = tkinter.Entry(self.container, textvariable=self.cell_y)
        self.cell_y_input.grid(row=2,column=1)

        self.container.pack()

    def get_move(self) -> circuit_generation.Move:
        return circuit_generation.Move(circuit_generation.Coll([7 * int(self.cell_y.get()) + int(self.cell_x.get())]))

