import tkinter
import numpy as np
import math
import random

class CNOT_input():
    def __init__(self, parent):
        self.container = tkinter.Frame(parent)

        self.targetx = None
        self.targety = None

        self.controlx = None
        self.controly = None

        self.control_label = tkinter.Label(self.container,text='control cell (X,Y):')
        self.control_label.grid(row=0,column=0)
        self.controlx_input = tkinter.Entry(self.container, textvariable=self.controlx)
        self.controlx_input.grid(row=0,column=1)
        self.controly_input = tkinter.Entry(self.container, textvariable=self.controly)
        self.controly_input.grid(row=0,column=2)

        self.target_label = tkinter.Label(self.container,text='target cell (X,Y):')
        self.target_label.grid(row=1,column=0)
        self.target_input = tkinter.Entry(self.container, textvariable=self.targetx)
        self.target_input.grid(row=1,column=1)
        self.target_input = tkinter.Entry(self.container, textvariable=self.targety)
        self.target_input.grid(row=1,column=2)

        self.container.pack()