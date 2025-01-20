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

    def set_vector(self, col: int, row: int, vector: np.ndarray, move_num: int):
        # Get the current color scheme for the bloch vectors
        existing_colors = self.spheres[col][row].vector_color
        existing_colors_filtered = [x for x in existing_colors if x is not None]

        self.spheres[col][row].clear()
        
        if np.sum(vector**2) < 0.5: #bell state case
            if len(existing_colors_filtered) == 0:
                # create hex codes based on move number, RGB has 6 hex digits. thus modulo 256^3 is taken
                vec_color = "#" + "%0.6X" % ((move_num * 127) % (256**3))
                vec_color2 = "#" + "%0.6X" % ((move_num * 119) % (256**3))

                self.spheres[col][row].vector_color = [vec_color, vec_color2]
            else: # for when the bloch sphere was entangled in a previous move
                self.spheres[col][row].vector_color = existing_colors_filtered

            self.spheres[col][row].add_vectors(1.1*np.array([0.,0.,1.]))
            self.spheres[col][row].add_vectors(1.1*np.array([0.,0.,-1.]))
        else: # normal case
            self.spheres[col][row].add_vectors(1.1*vector)
        self.spheres[col][row].render()

