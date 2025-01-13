from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
 
matrix = [[0, 0, 0, 1],
          [0, 0, 1, 0],
          [1, 0, 0, 0],
          [0, 1, 0, 0]]
gate = UnitaryGate(matrix)
 
circuit = QuantumCircuit(2)
circuit.append(gate, [0, 1])

circuit.draw("mpl")