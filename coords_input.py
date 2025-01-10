import tkinter
import numpy as np
import math
import random

# creates the input scale for each column
# @input parent: the parent widget for these columns
# @return: an array with 7 scale objects.
def create_coords_inputs(parent):
    columns_inputs = []
    for col in range(0,7):
        columns_inputs.append(tkinter.Scale(parent, orient="vertical", from_=1.0, to=0.0, resolution=0.1))
        columns_inputs[col].grid(row=0, column=col)

    return columns_inputs

