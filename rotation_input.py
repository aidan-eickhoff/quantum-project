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
        self.axis = tkinter.StringVar()

        self.X_option = tkinter.Radiobutton(self.container, text='X', variable=self.axis, value='X')
        self.X_option.grid(row=0,column=0)
        self.Y_option = tkinter.Radiobutton(self.container, text='Y', variable=self.axis, value='Y')
        self.Y_option.grid(row=0,column=1)
        self.Z_option = tkinter.Radiobutton(self.container, text='Z', variable=self.axis, value='Z')
        self.Z_option.grid(row=0,column=2)

        self.cell_label = tkinter.Label(self.container,text='cell (X,Y):')
        self.cell_label.grid(row=1,column=0)
        self.cellx_input = tkinter.Entry(self.container, textvariable=self.cellx)
        self.cellx_input.grid(row=1,column=1)
        self.celly_input = tkinter.Entry(self.container, textvariable=self.celly)
        self.celly_input.grid(row=1,column=2)

        self.angle_label = tkinter.Label(self.container,text='Angle (deg):')
        self.angle_label.grid(row=2,column=0)
        self.angle_input = tkinter.Entry(self.container, textvariable=self.angle)
        self.angle_input.grid(row=2,column=1,columnspan=2)

        self.container.pack()

    

