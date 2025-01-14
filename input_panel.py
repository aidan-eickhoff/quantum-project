import tkinter
import numpy as np
import math
import random
from rotation_input import Rotation_input
from CY_input import CY_input

class Input_panel():
    def __init__(self, parent, add_move):
        self.container = tkinter.Frame(parent, borderwidth=2, relief=tkinter.RIDGE)

        self.move_type_container = tkinter.Frame(self.container, borderwidth=2, relief=tkinter.RIDGE, padx=10,pady=5)
        self.move_type_container.grid(row=0,column=1)

        # attributes for the diffrent move inputs, starts with rotate input
        self.superpos_input = Rotation_input(self.move_type_container)
        self.entanglement_input = CY_input(self.move_type_container)
        self.entanglement_input.container.pack_forget() # hides CY input

        #switch move buttons
        self.move_select_container = tkinter.Frame(self.container, borderwidth=2, relief=tkinter.RIDGE)
        self.move_type: int = 0
        self.move_type_superposition = tkinter.Button(self.move_select_container, text='rotation move', command=self.show_superposition_inputs, state="disabled")
        self.move_type_superposition.grid(row=0, column=0, sticky="ew")

        self.move_type_entanglement = tkinter.Button(self.move_select_container, text='CY move', command=self.show_entanglement_inputs)
        self.move_type_entanglement.grid(row=1, column=0, sticky="ew")

        self.move_select_container.grid(row=0,column=0,sticky="ns")

        #submit_move button
        self.submit_button = tkinter.Button(self.container, text='Play move', command=add_move)
        self.submit_button.grid(row=1, columnspan=2, sticky="ew")

    def clear_input(self):
        for child in self.move_type_container.winfo_children():
            child.pack_forget()
    
    def show_superposition_inputs(self):
        self.move_type_superposition["state"] = "disabled"
        self.move_type_entanglement["state"] = "normal"
        self.clear_input()
        self.superpos_input.container.pack()# = Rotation_input(self.move_type_container)

    def show_entanglement_inputs(self):
        self.move_type_entanglement["state"] = "disabled"
        self.move_type_superposition["state"] = "normal"
        self.clear_input()
        self.entanglement_input.container.pack() #= CY_input(self.move_type_container)