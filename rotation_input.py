import tkinter
import numpy as np
import math
import random

class Rotation_input():
    def __init__(self, parent):
        self.container = tkinter.Frame(parent)

        self.cellx = None
        self.celly = None
        self.angle = 0
        self.rotate_vec_x = 0
        self.rotate_vec_z = 0

        self.cell_label = tkinter.Label(self.container,text='Rotation move')
        self.cell_label.grid(row=0,column=0, columnspan=2)

        self.cell_label = tkinter.Label(self.container,text='Cell (X,Y)')
        self.cell_label.grid(row=1,column=0)
        self.cellx_input = tkinter.Entry(self.container, textvariable=self.cellx)
        self.cellx_input.grid(row=2,column=0)
        self.celly_input = tkinter.Entry(self.container, textvariable=self.celly)
        self.celly_input.grid(row=2,column=1)

        self.cell_label = tkinter.Label(self.container,text='Rotation vector (X,Z)')
        self.cell_label.grid(row=3,column=0)
        self.cellx_input = tkinter.Entry(self.container, textvariable=self.rotate_vec_x)
        self.cellx_input.grid(row=4,column=0)
        self.celly_input = tkinter.Entry(self.container, textvariable=self.rotate_vec_z)
        self.celly_input.grid(row=4,column=1)

        self.angle_label = tkinter.Label(self.container,text='Rotation angle (deg)')
        self.angle_label.grid(row=5,column=0)
        self.angle_input = tkinter.Entry(self.container, textvariable=self.angle)
        self.angle_input.grid(row=6,column=0)

        self.container.pack()

    

