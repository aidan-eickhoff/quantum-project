from qiskit import *
from qiskit.circuit.quantumcircuit import *
from qiskit.primitives.containers import BitArray
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import *
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerOptions, SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import *

from enum import Enum
import numpy as np

# Superclasses
class Move():
    def __init__(self, gate: Gate):
        self.gate: Gate = gate

    def __str__(self) -> str:
        return self.gate.__str__()

class Gate():
    def __init__(self, slots: list[int]):
        self.slots: list[int] = slots

class Axis(Enum):
    X = 0
    Y = 1
    Z = 2

# 1 qubit gates
class RX(Gate):
    def __init__(self, angle: float, qubits: list[int]):
        if len(qubits) != 1:
            print("RX gate should affect 1 qubit.")
            return
        super().__init__(qubits)
        self.angle: float = angle
        self.target = qubits[0]

    def __str__(self) -> str:
        return "RX: " + str(self.slots[0])

class RY(Gate):
    def __init__(self, angle: float, qubits: list[int]):
        if len(qubits) != 1:
            print("RY gate should affect 1 qubit.")
            return
        super().__init__(qubits)
        self.angle: float = angle
        self.target = qubits[0]

    def __str__(self) -> str:
        return "RY: " + str(self.slots[0])

class RZ(Gate):
    def __init__(self, angle: float, qubits: list[int]):
        if len(qubits) != 1:
            print("RZ gate should affect 1 qubit.")
            return
        super().__init__(qubits)
        self.angle: float = angle
        self.target = qubits[0]

    def __str__(self) -> str:
        return "RZ: " + str(self.slots[0])

class RV(Gate):
    def __init__(self, rot_axis: np.array, rot_angle: float, qubits: list[int]):
        if len(qubits) != 1:
            print("RV gate should affect 1 qubit.")
            return
        if len(rot_axis) != 3:
            print("RV gate rotation axis should have 3 components")
            return
        super().__init__(qubits)
        self.rot_axis: np.array = rot_axis/np.sqrt(np.dot(rot_axis, rot_axis))
        self.rot_angle: float = rot_angle
        self.target = qubits[0]

    def __str__(self) -> str:
        return "RZ: " + str(self.slots[0])

class H(Gate):
    def __init__(self, qubits: list[int]):
        super().__init__(qubits)
        if len(qubits) != 1:
            print("H gate should affect 1 qubit.")
            return

        self.target = qubits[0]
    
    def __str__(self) -> str:
        return "H: " + str(self.target)

# 2 qubit gates
class CX(Gate):
    def __init__(self, qubits: list[int]):
        if len(qubits) != 2:
            print("CX gate should affect 2 qubit.")
            return
        super().__init__(qubits)
        self.control = qubits[0]
        self.target = qubits[1]        

    def __str__(self) -> str:
        return "CX, control: " + str(self.control) +", target: " + str(self.target)

class CY(Gate):
    def __init__(self, qubits: list[int]):
        if len(qubits) != 2:
            print("CY gate should affect 2 qubit.")
            return
        super().__init__(qubits)
        self.control = qubits[0]
        self.target = qubits[1]        

    def __str__(self) -> str:
        return "CY, control: " + str(self.control) +", target: " + str(self.target)

class CZ(Gate):
    def __init__(self, qubits: list[int]):
        if len(qubits) != 2:
            print("CZ gate should affect 2 qubit.")
            return
        super().__init__(qubits)
        self.control = qubits[0]
        self.target = qubits[1]        

    def __str__(self) -> str:
        return "CZ, control: " + str(self.control) +", target: " + str(self.target)

class SWAP(Gate):
    def __init__(self, qubits: list[int]):
        if len(qubits) != 2:
            print("SWAP gate should affect 2 qubit.")
            return
        super().__init__(qubits)

    def __str__(self) -> str:
        return "SWAP, control: " + str(self.control) +", target: " + str(self.target)

# Util functions
def run_circuit(qc: QuantumCircuit, numShots: int=10, isPhysical: bool=False, hasNoise: bool=False):

    # Define which backend to use
    if isPhysical:
        service = QiskitRuntimeService(channel="ibm_quantum", token=token)
        backend = service.least_busy(operational=True, simulator=False)
    elif hasNoise:
        backend = FakeWashingtonV2()
    else:
        backend = AerSimulator()

    # Compile circuit for chosen backend 
    pm = generate_preset_pass_manager(backend=backend, optimization_level=3)
    isa_circuit = pm.run(qc)

    # Create sampler that will run the amount of shots specified
    options = SamplerOptions(default_shots=numShots)
    sampler = Sampler(backend, options)

    # Run sampler on compiled circuit
    return sampler.run([isa_circuit]).result()

def generate_mappings(unique_qubits: set[int]) -> tuple[dict[int, int], dict[int, int]]:
    """Generates a mapping of board index to qubit index, and vice versa.\\
    `mapping_qb[qubit_index] = board_index`\\
    `mapping_bq[board_index] = qubit_index`
    """
    mapping_qb: dict[int, int] = dict()
    for qubit_index, board_index in enumerate(unique_qubits):
        mapping_qb[qubit_index] = board_index
        
    mapping_bq: dict[int, int] = dict()
    for key in mapping_qb.keys():
        mapping_bq[mapping_qb.get(key)] = key

    return (mapping_qb, mapping_bq)

def generate_seperation(moves: list[Move]) -> list[frozenset[int]]:
    """Generates a seperation of qubits into sets.\\
        The sets are arranged s.t. only qubits within a set interact togther.
        This means one simulation can be used per set.
    """
    # Count number of necessary qubits
    unique_qubits: set[int] = set()
    for move in moves:
        for qubit in move.gate.slots:
            unique_qubits.add(qubit)

    # Create a set for each qubit
    qubit_set_list: list[set[int]] = list()
    for qubit in unique_qubits:
        qubit_set_list.append(set([qubit]))
    
    # For each move, union the sets of the qubits it contains
    for move in moves:
        # Find sets containing used qubits
        sets = list()
        for qubit in move.gate.slots:
            for qubit_set in qubit_set_list:
                if qubit in qubit_set:
                    sets.append(qubit_set)
        
        # Union found sets into one, remove them, and insert the union
        union: set[int] = set()
        for qubit_set in sets:
            union = union.union(qubit_set)
            qubit_set_list.remove(qubit_set)
        qubit_set_list.append(union)

    # Freeze sets (so they can be used as index later)
    return [frozenset(x) for x in qubit_set_list]

# Circuit generators
def generate_physical_circuit(moves: list[Move], measurement_axes: set[Axis] = set([Axis.X, Axis.Y, Axis.Z])) -> QuantumCircuit:
    # Count number of necessary qubits
    unique_qubits: set = set()
    for move in moves:
        for qubit in move.gate.slots:
            unique_qubits.add(qubit)

    _, mapping_bq = generate_mappings(unique_qubits)

    # Create quantum circuit
    q_num = len(unique_qubits)
    qReg_x = QuantumRegister(q_num, "qReg_x")
    cReg_x = ClassicalRegister(q_num, "cReg_x")
    qReg_y = QuantumRegister(q_num, "qReg_y")
    cReg_y = ClassicalRegister(q_num, "cReg_y")
    qReg_z = QuantumRegister(q_num, "qReg_z")
    cReg_z = ClassicalRegister(q_num, "cReg_z")
    
    regs = []
    if Axis.X in measurement_axes:
        regs.append(qReg_x)
        regs.append(cReg_x)
    if Axis.Y in measurement_axes:
        regs.append(qReg_y)
        regs.append(cReg_y)
    if Axis.Z in measurement_axes:
        regs.append(qReg_z)
        regs.append(cReg_z)

    qc = QuantumCircuit(*regs)
    for move in moves:
        gate = move.gate
        match gate:
            # 1 qubit gates
            case RX():
                if Axis.X in measurement_axes:
                    qc.rx(gate.angle, qReg_x[mapping_bq[gate.target]])
                if Axis.Y in measurement_axes:
                    qc.rx(gate.angle, qReg_y[mapping_bq[gate.target]])
                if Axis.Z in measurement_axes:
                    qc.rx(gate.angle, qReg_z[mapping_bq[gate.target]])
            case RY():
                if Axis.X in measurement_axes:
                    qc.ry(gate.angle, qReg_x[mapping_bq[gate.target]])
                if Axis.Y in measurement_axes:
                    qc.ry(gate.angle, qReg_y[mapping_bq[gate.target]])
                if Axis.Z in measurement_axes:
                    qc.ry(gate.angle, qReg_z[mapping_bq[gate.target]])
            case RZ():
                if Axis.X in measurement_axes:
                    qc.rz(gate.angle, qReg_x[mapping_bq[gate.target]])
                if Axis.Y in measurement_axes:
                    qc.rz(gate.angle, qReg_y[mapping_bq[gate.target]])
                if Axis.Z in measurement_axes:
                    qc.rz(gate.angle, qReg_z[mapping_bq[gate.target]])
            case RV():
                if Axis.X in measurement_axes:
                    qc.rv(*(gate.rot_axis * gate.rot_angle), qReg_x[mapping_bq[gate.target]])
                if Axis.Y in measurement_axes:
                    qc.rv(*(gate.rot_axis * gate.rot_angle), qReg_y[mapping_bq[gate.target]])
                if Axis.Z in measurement_axes:
                    qc.rv(*(gate.rot_axis * gate.rot_angle), qReg_z[mapping_bq[gate.target]])
            case H():
                if Axis.X in measurement_axes:
                    qc.h(qReg_x[mapping_bq[gate.target]])
                if Axis.Y in measurement_axes:
                    qc.h(qReg_y[mapping_bq[gate.target]])
                if Axis.Z in measurement_axes:
                    qc.h(qReg_z[mapping_bq[gate.target]])
            
            # 2 qubit gates
            case CX():
                if Axis.X in measurement_axes:
                    qc.cx(qReg_x[mapping_bq[gate.control]], qReg_x[mapping_bq[gate.target]])
                if Axis.Y in measurement_axes:
                    qc.cx(qReg_y[mapping_bq[gate.control]], qReg_y[mapping_bq[gate.target]])
                if Axis.Z in measurement_axes:
                    qc.cx(qReg_z[mapping_bq[gate.control]], qReg_z[mapping_bq[gate.target]])

            case CY():
                if Axis.X in measurement_axes:
                    qc.cy(qReg_x[mapping_bq[gate.control]], qReg_x[mapping_bq[gate.target]])
                if Axis.Y in measurement_axes:
                    qc.cy(qReg_y[mapping_bq[gate.control]], qReg_y[mapping_bq[gate.target]])
                if Axis.Z in measurement_axes:
                    qc.cy(qReg_z[mapping_bq[gate.control]], qReg_z[mapping_bq[gate.target]])

            case CZ():
                if Axis.X in measurement_axes:
                    qc.cz(qReg_x[mapping_bq[gate.control]], qReg_x[mapping_bq[gate.target]])
                if Axis.Y in measurement_axes:
                    qc.cz(qReg_y[mapping_bq[gate.control]], qReg_y[mapping_bq[gate.target]])
                if Axis.Z in measurement_axes:
                    qc.cz(qReg_z[mapping_bq[gate.control]], qReg_z[mapping_bq[gate.target]])

            case SWAP():
                if Axis.X in measurement_axes:
                    qc.swap(qReg_x[mapping_bq[gate.slots[0]]], qReg_x[mapping_bq[gate.slots[1]]])
                if Axis.Y in measurement_axes:
                    qc.swap(qReg_y[mapping_bq[gate.slots[0]]], qReg_y[mapping_bq[gate.slots[1]]])
                if Axis.Z in measurement_axes:
                    qc.swap(qReg_z[mapping_bq[gate.slots[0]]], qReg_z[mapping_bq[gate.slots[1]]])

    if Axis.X in measurement_axes:
        qc.h(qReg_x)
        qc.measure(qReg_x, cReg_x)
    if Axis.Y in measurement_axes:
        v = np.pi/np.sqrt(2)
        qc.rv(0, v, v, qReg_z)
        qc.measure(qReg_y, cReg_y)
    if Axis.Z in measurement_axes:
        qc.measure(qReg_z, cReg_z)

    return qc

def generate_simulator_circuits(moves: list[Move]) -> list[QuantumCircuit]:
    qubit_set_list: list[frozenset[int]] = generate_seperation(moves)

    # For each set, find the moves that affect it
    moves_per_set: dict[frozenset[int], list[Move]] = dict()
    for qubit_set in qubit_set_list:
        moves_per_set[qubit_set] = list()
        for move in moves:
            if all(s in qubit_set for s in move.gate.slots):
                moves_per_set[qubit_set].append(move)

            elif any(s in qubit_set for s in move.gate.slots):
                # This should not happen
                print("ERROR")

    qcs: list[QuantumCircuit] = list()
    for move_sublist in moves_per_set.values():
        qcs.append(generate_physical_circuit(move_sublist, set([Axis.X])))
        qcs.append(generate_physical_circuit(move_sublist, set([Axis.Y])))
        qcs.append(generate_physical_circuit(move_sublist, set([Axis.Z])))

    return qcs
        
def run_moves(moves: list[Move], isPhysical = False):
    if isPhysical:
        qc = generate_physical_circuit(moves)
        result = run_circuit(qc, 1, False)
        cReg_x = result[0].data.cReg_x.array
        cReg_y = result[0].data.cReg_y.array
        cReg_z = result[0].data.cReg_z.array
        return (cReg_x, cReg_y, cReg_z)
    else:
        qcs = generate_simulator_circuits(moves)
        results = [run_circuit(qc, 1)[0].data for qc in qcs]
        results_x = []
        results_y = []
        results_z = []
        for i in range(int(len(results)/3)):
            results_x.append(results[3*i])
            results_y.append(results[3*i+1])
            results_z.append(results[3*i+2])

        cReg_x = BitArray.concatenate_bits([i.cReg_x for i in results_x]).array
        cReg_y = BitArray.concatenate_bits([i.cReg_y for i in results_y]).array
        cReg_z = BitArray.concatenate_bits([i.cReg_z for i in results_z]).array
        return (cReg_x, cReg_y, cReg_z)

r = run_moves([Move(RX(-np.pi/2, [1]))])
print(r)

