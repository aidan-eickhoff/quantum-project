import qutip
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BlochVisualizer:
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.spheres = [[self.make_bloch_sphere(i, j) for i in range(7)] for j in range(6)]
                

    def make_bloch_sphere(self, col, row) -> tuple[qutip.Bloch, FigureCanvasTkAgg]:
        fig = Figure(figsize = (1, 1), dpi = 150)
        
        b = qutip.Bloch(fig)
        b.add_vectors([1.1 / np.sqrt(2), 1.1/np.sqrt(2),0], colors=["#f00"])
        # b.add_vectors([1 / np.sqrt(2), -1/np.sqrt(2),0], colors=["#f00"])

        b.font_size = 8
        b.vector_width = 1
        b.frame_width = 0.5
        b.sphere_alpha = 0.1
        b.frame_alpha = 0.05
        b.render()
    
        canvas = FigureCanvasTkAgg(fig, master = self.container)  
        canvas.draw()
        canvas.get_tk_widget().grid(row=row, column=col)

        return (b, canvas)
