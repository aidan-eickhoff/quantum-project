import qutip
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BlochVisualizer:
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.spheres: list[list[tuple[qutip.Bloch, FigureCanvasTkAgg]]] = [[self.make_bloch_sphere(j, i) for i in range(6)] for j in range(7)]
                

    def make_bloch_sphere(self, col: int, row: int) -> tuple[qutip.Bloch, FigureCanvasTkAgg]:
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

        return (b, canvas)

    def add_vector(self, col: int, row: int, vector: tuple[float, float, float]):
        self.spheres[col][row][0].add_vectors(vector);
        self.spheres[col][row][0].render();

