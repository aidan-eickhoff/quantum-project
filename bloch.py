import qutip
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BlochVisualizer:
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.spheres: list[list[qutip.Bloch]] = [[self.make_bloch_sphere(i, j) for i in range(6)] for j in range(7)]
                

    def make_bloch_sphere(self, col: int, row: int) -> qutip.Bloch:
        fig = Figure(figsize = (1, 1), dpi = 150)
        
        b = qutip.Bloch(fig)

        b.font_size = 8
        b.vector_width = 1
        b.frame_width = 0.5
        b.sphere_alpha = 0.1
        b.frame_alpha = 0.05
        b.render()

        canvas = FigureCanvasTkAgg(fig, master = self.container)  
        canvas.draw()
        canvas.get_tk_widget().grid(column=col, row=row)

        return b

    def set_vector(self, col: int, row: int, vector: np.ndarray):
        vector *= 1.1 / np.linalg.norm(vector)
        print(vector)
        self.spheres[col][row].clear()
        self.spheres[col][row].add_vectors(vector);
        self.spheres[col][row].render();

