import tkinter
import circuit_generation
import numpy as np

class Swap_input():
    def __init__(self, parent):
        self.container = tkinter.Frame(parent)

        self.targetx = tkinter.StringVar()
        self.targety = tkinter.StringVar()

        self.controlx = tkinter.StringVar()
        self.controly = tkinter.StringVar()

        self.control_label = tkinter.Label(self.container,text='Swap move')
        self.control_label.grid(row=0,column=0, columnspan=2)

        self.control_label = tkinter.Label(self.container,text='Control cell (X,Y)')
        self.control_label.grid(row=1,column=0)
        self.controlx_input = tkinter.Entry(self.container, textvariable=self.controlx)
        self.controlx_input.grid(row=2,column=0)
        self.controly_input = tkinter.Entry(self.container, textvariable=self.controly)
        self.controly_input.grid(row=2,column=1)

        self.target_label = tkinter.Label(self.container,text='Target cell (X,Y)')
        self.target_label.grid(row=3,column=0)
        self.target_input = tkinter.Entry(self.container, textvariable=self.targetx)
        self.target_input.grid(row=4,column=0)
        self.target_input = tkinter.Entry(self.container, textvariable=self.targety)
        self.target_input.grid(row=4,column=1)

        self.container.pack()

    def get_move(self) -> circuit_generation.Move:
        return circuit_generation.Move(circuit_generation.SWAP(
                                    [7 * int(self.controly.get()) + int(self.controlx.get()),
                                      7 * int(self.targety.get()) + int(self.targetx.get())]))