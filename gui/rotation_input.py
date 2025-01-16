import tkinter
import circuit_generation
import numpy as np

class Rotation_input():
    def __init__(self, parent):
        self.container = tkinter.Frame(parent)

        self.cellx = tkinter.StringVar()
        self.celly = tkinter.StringVar()
        self.angle = tkinter.StringVar()
        self.rotate_vec_x = tkinter.StringVar()
        self.rotate_vec_z = tkinter.StringVar()

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
        self.rotationx_input = tkinter.Entry(self.container, textvariable=self.rotate_vec_x)
        self.rotationx_input.grid(row=4,column=0)
        self.rotationz_input = tkinter.Entry(self.container, textvariable=self.rotate_vec_z)
        self.rotationz_input.grid(row=4,column=1)

        self.angle_label = tkinter.Label(self.container, text='Rotation angle (deg)')
        self.angle_label.grid(row=5,column=0)
        self.angle_input = tkinter.Entry(self.container, textvariable=self.angle)
        self.angle_input.grid(row=6,column=0)

        self.container.pack()

    def get_move(self) -> circuit_generation.Move:
        return circuit_generation.Move(circuit_generation.RV(np.array(
            [float(self.rotate_vec_x.get()), 0., float(self.rotate_vec_z.get())]), 
            float(self.angle.get()) * np.pi/180,
            [7 * int(self.celly.get()) + int(self.cellx.get())]
            ))

    

