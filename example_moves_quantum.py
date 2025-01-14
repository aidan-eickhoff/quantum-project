import qiskit
import math
import numpy as np
pi = math.pi

moves = {}
moves["1"] = {"type": "single",
              "column": 3, # start indexing at zero
              "row": 0,
              "vector": np.array([1,0,1]),
              "magnitude": pi / 2
            }

def set_vector_to_right_size(move:dict)->None:
    if not move["type"] == "single":
        raise ValueError("This function only works for single qubit gates / moves")
    # step 1: normalise vector
    vector:np.array = move["vector"]
    length = np.sqrt(vector.dot(vector))
    vector = vector / length
    # step 2: set the magnitude of the vector
    magnitude = move["magnitude"]
    vector = vector * magnitude
    # set vector in the move
    move["vector"] = vector
    return

