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


        self.title_label = tkinter.Label(self.container,text='Measurement move')
        self.title_label.grid(row=0,column=0, columnspan=6)

        self.meas_label = tkinter.Label(self.container,text='Measuring vector (X,Y,Z)', justify="left", anchor="w")
        self.meas_label.grid(row=1,column=0, columnspan=6, sticky = "w")
        self.meas_x_input = tkinter.Entry(self.container, textvariable=self.meas_x, width=13)
        self.meas_x_input.grid(row=2,column=0, columnspan=2)
        self.meas_y_input = tkinter.Entry(self.container, textvariable=self.meas_y, width=13)
        self.meas_y_input.grid(row=2,column=2, columnspan=2)
        self.meas_z_input = tkinter.Entry(self.container, textvariable=self.meas_z, width=13)
        self.meas_z_input.grid(row=2,column=4, columnspan=2)

        self.cell_label = tkinter.Label(self.container,text='Cell (X,Y)', justify="left", anchor="w")
        self.cell_label.grid(row=3,column=0, columnspan=6, sticky = "w")
        self.cell_x_input = tkinter.Entry(self.container, textvariable=self.cell_x)
        self.cell_x_input.grid(row=4,column=0, columnspan=3)
        self.cell_y_input = tkinter.Entry(self.container, textvariable=self.cell_y)
        self.cell_y_input.grid(row=4,column=3, columnspan=3)


        self.container.pack()

    def get_move(self) -> circuit_generation.Move:
        return circuit_generation.Move(circuit_generation.Meas(
            np.array(
                list(map(float, [self.meas_x.get(), self.meas_y.get(), self.meas_z.get()]))
            ),
            [7 * int(self.cell_y.get()) + int(self.cell_x.get())]
        ))
