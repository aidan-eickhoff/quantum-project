import qutip
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BlochVisualizer:
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.bloch_height: int = int(parent.winfo_screenheight()/7)

        self.spheres: list[list[qutip.Bloch]] = [[self.make_bloch_sphere(i, j) for i in range(7)] for j in range(6)]
        self.set_measured_color(0,0,False)
        
    def make_bloch_sphere(self, col: int, row: int) -> qutip.Bloch:
        fig = Figure(figsize = (1, 1), dpi=self.bloch_height)
        
        b = qutip.Bloch(fig)

        b.font_size = 8
        b.vector_width = 1
        b.frame_width = 0.5
        b.sphere_alpha = 0.1
        b.frame_alpha = 0.05
        b.render()

        canvas = FigureCanvasTkAgg(fig, master = self.container)  
        canvas.draw()
        canvas.get_tk_widget().grid(column=col, row=5-row)

        return b

    def set_vector(self, col: int, row: int, vector: np.ndarray):
        self.spheres[col][row].clear()
        self.spheres[col][row].add_vectors(1.1*vector)
        self.spheres[col][row].render()

    def set_measured_color(self, col: int, row: int, isRed: bool):
        b = self.spheres[col][row]
        b.clear()
        if isRed:
            b.sphere_color = "#FF0000"
        else:
            b.sphere_color = "#ffff66"
        b.sphere_alpha = 1
        b.xlabel = 	["",""]
        b.ylabel = 	["",""]
        b.zlabel = 	["",""]
        b.frame = False
        b.vector_width = 0
        b.render()