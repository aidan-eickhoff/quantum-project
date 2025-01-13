import tkinter
import numpy as np
import math
import random
from rotation_input import Rotation_input
from CNOT_input import CNOT_input

class Input_panel():
    def __init__(self, parent, add_move):
        self.container = tkinter.Frame(parent)

        #create superposition inputs
        self.move_type_container = tkinter.Frame(self.container)
        self.move_type_container.grid(row=0,column=1,rowspan=2)

        # moves input attributes
        self.superpos_input = Rotation_input(self.move_type_container)
        self.entanglement_input = None

        #switch move buttons
        self.move_type: int = 0
        self.move_type_superposition = tkinter.Button(self.container, text='rotation move', command=self.show_superposition_inputs)
        self.move_type_superposition.grid(row=0, column=0)

        self.move_type_entanglement = tkinter.Button(self.container, text='CNOT move', command=self.show_entanglement_inputs)
        self.move_type_entanglement.grid(row=1, column=0)

        #submit_move button
        self.submit_button = tkinter.Button(self.container, text='Input move', command=add_move)
        self.submit_button.grid(row=3, columnspan=8)
        self.container.pack()

    def clear_input(self):
        for child in self.move_type_container.winfo_children():
            child.destroy()
    
    def show_superposition_inputs(self):
        self.clear_input()
        self.superpos_input = Rotation_input(self.move_type_container)

    def show_entanglement_inputs(self):
        self.clear_input()
        self.entanglement_input = CNOT_input(self.move_type_container)