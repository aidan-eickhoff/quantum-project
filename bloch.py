import qutip
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BlochVisualizer:
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.bloch_height: int = int(parent.winfo_screenheight()/7)

<<<<<<< HEAD
=======
        self.tk_objects: list[list[FigureCanvasTkAgg]] = [[None for row in range(6)] for col in range(7)]
>>>>>>> 560546a (collapse colors)
        self.spheres: list[list[qutip.Bloch]] = [[self.make_bloch_sphere(col, row) for row in range(6)] for col in range(7)]
        
    def make_bloch_sphere(self, col: int, row: int) -> qutip.Bloch:
        fig = Figure(figsize = (1, 1), dpi=self.bloch_height)
        
        b = qutip.Bloch(fig)

        b.font_size = 8
        b.vector_width = 1
        b.frame_width = 0.5
        b.sphere_alpha = 0.1
        b.frame_alpha = 0.05
        b.add_vectors(np.array([0,0,1.1]))
        b.render()

        canvas = FigureCanvasTkAgg(fig, master = self.container)  
        canvas.draw()
        canvas.get_tk_widget().grid(column=col, row=5-row)

        return b

    def set_vector(self, col: int, row: int, vector: np.ndarray):
        self.spheres[col][row].clear()
        self.spheres[col][row].add_vectors(1.1*vector)
        self.spheres[col][row].render()

<<<<<<< HEAD
    def set_color(self, col: int, row: int, color: str):
        self.spheres[col][row].vector_color = [color]
        self.spheres[col][row].render()

=======
>>>>>>> 560546a (collapse colors)
    def set_collapsed_color(self, col: int, row: int, is_red: bool):
        self.spheres[col][row].clear()
        self.spheres[col][row].sphere_alpha = 1
        self.spheres[col][row].sphere_color = "#f00" if is_red else "#ff0"
        self.spheres[col][row].frame_alpha = 0.
        self.spheres[col][row].xlabel = ['', '']
        self.spheres[col][row].ylabel = ['', '']
        self.spheres[col][row].zlabel = ['', '']
        self.spheres[col][row].render()
<<<<<<< HEAD
=======
        # self.collapsed_canvas = tk.Canvas(self.container).grid()

>>>>>>> 560546a (collapse colors)
