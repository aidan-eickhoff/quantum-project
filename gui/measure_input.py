import tkinter
import circuit_generation
import numpy as np

class Measure_input():
    def __init__(self, parent):
        self.container = tkinter.Frame(parent)
        self.meas_x = tkinter.StringVar()
        self.meas_y = tkinter.StringVar()
        self.meas_z = tkinter.StringVar()
        
        self.cell_x = tkinter.StringVar()
        self.cell_y = tkinter.StringVar()


        self.cell_label = tkinter.Label(self.container,text='Measurement move')
        self.cell_label.grid(row=0,column=0, columnspan=2)

        self.cell_label = tkinter.Label(self.container,text='Measuring vector (X,Y,Z)')
        self.cell_label.grid(row=1,column=0)
        self.meas_x_input = tkinter.Entry(self.container, textvariable=self.meas_x)
        self.meas_x_input.grid(row=2,column=0)
        self.meas_y_input = tkinter.Entry(self.container, textvariable=self.meas_y)
        self.meas_y_input.grid(row=3,column=0)
        self.meas_z_input = tkinter.Entry(self.container, textvariable=self.meas_z)
        self.meas_z_input.grid(row=4,column=0)

        self.cell_label = tkinter.Label(self.container,text='Cell (X,Y)')
        self.cell_label.grid(row=1,column=1)
        self.cell_x_input = tkinter.Entry(self.container, textvariable=self.cell_x)
        self.cell_x_input.grid(row=2,column=1)
        self.cell_y_input = tkinter.Entry(self.container, textvariable=self.cell_y)
        self.cell_y_input.grid(row=3,column=1)


        self.container.pack()

    def get_move(self) -> circuit_generation.Move:
        return circuit_generation.Move(circuit_generation.Meas(
            np.array(
                list(map(float, [self.meas_x.get(), self.meas_y.get(), self.meas_z.get()]))
            ),
            [7 * int(self.cell_y.get()) + int(self.cell_x.get())]
        ))
