from qiskit import *
from qiskit.circuit.quantumcircuit import *
from qiskit.primitives.containers import BitArray
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import *
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerOptions, SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import *

from abc import ABC, abstractmethod
from enum import Enum
import numpy as np

# Superclasses
class Move():
    def __init__(self, gate: Gate):
        self.gate: Gate = gate

    def __str__(self) -> str:
        return self.gate.__str__()

class Gate(ABC):
    def __init__(self, slots: list[int]):
        self.slots: list[int] = slots

    @abstractmethod
    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        pass

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
        x_pos = self.slots[0] % 7
        y_pos = int((self.slots[0] - x_pos) / 7)
        return "RX: (" + str(x_pos) + "," + str(y_pos) + ")"

    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.rx(self.angle, qReg[mapping_bq[self.target]]) 

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
    
    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.ry(self.angle, qReg[mapping_bq[self.target]]) 

class RZ(Gate):
    def __init__(self, angle: float, qubits: list[int]):
        if len(qubits) != 1:
            print("RZ gate should affect 1 qubit.")
            return
        super().__init__(qubits)
        self.angle: float = angle
        self.target = qubits[0]

    def __str__(self) -> str:
        x_pos = self.slots[0] % 7
        y_pos = int((self.slots[0] - x_pos) / 7)
        return "RZ: (" + str(x_pos) + "," + str(y_pos) + ")"

    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.rz(self.angle, qReg[mapping_bq[self.target]]) 

class RV(Gate):
    def __init__(self, rot_axis: np.array, rot_angle: float, qubits: list[int]):
        if len(qubits) != 1:
            print("RV gate should affect 1 qubit.")
            return
        if len(rot_axis) != 3:
            print("RV gate rotation axis should have 3 components")
            return
        super().__init__(qubits)
        self.rot_axis: np.array = rot_axis / np.linalg.norm(rot_axis)
        self.rot_angle: float = rot_angle
        self.target = qubits[0]

    def __str__(self) -> str:
        x_pos = self.slots[0] % 7
        y_pos = int((self.slots[0] - x_pos) / 7)
        return "RV: (" + str(x_pos) + "," + str(y_pos) + ")"
    
    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.rv(*(self.rot_axis * self.rot_angle), qReg[mapping_bq[self.target]])

class H(Gate):
    def __init__(self, qubits: list[int]):
        super().__init__(qubits)
        if len(qubits) != 1:
            print("H gate should affect 1 qubit.")
            return

        self.target = qubits[0]
    
    def __str__(self) -> str:
        return "H: " + str(self.target)

    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.h(qReg[mapping_bq[self.target]])

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

    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.cx(qReg[mapping_bq[self.control]], qReg[mapping_bq[self.target]])

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
    
    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.cy(qReg[mapping_bq[self.control]], qReg[mapping_bq[self.target]])

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

    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.cz(qReg[mapping_bq[self.control]], qReg[mapping_bq[self.target]])

class CRX(Gate):
    def __init__(self, angle, qubits: list[int]):
        if len(qubits) != 2:
            print("CRX gate should affect 2 qubit.")
            return
        super().__init__(qubits)
        self.control = qubits[0]
        self.target = qubits[1]
        self.angle = angle     

    def __str__(self) -> str:
        return "CRX, control: " + str(self.control) +", target: " + str(self.target)

    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.crx(self.angle, qReg[mapping_bq[self.control]], qReg[mapping_bq[self.target]])

class CRY(Gate):
    def __init__(self, angle, qubits: list[int]):
        if len(qubits) != 2:
            print("CRY gate should affect 2 qubit.")
            return
        super().__init__(qubits)
        self.control = qubits[0]
        self.target = qubits[1]
        self.angle = angle     

    def __str__(self) -> str:
        c_x_pos = self.control % 7
        c_y_pos = int((self.control - c_x_pos) / 7)
        t_x_pos = self.target % 7
        t_y_pos = int((self.target - t_x_pos) / 7)

        return "CRY: control=(" + str(c_x_pos) + "," + str(c_y_pos) + "), target=" + "(" + str(t_x_pos) + "," + str(t_y_pos) + ")"

    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.cry(self.angle, qReg[mapping_bq[self.control]], qReg[mapping_bq[self.target]])

class CRZ(Gate):
    def __init__(self, angle, qubits: list[int]):
        if len(qubits) != 2:
            print("CRZ gate should affect 2 qubit.")
            return
        super().__init__(qubits)
        self.control = qubits[0]
        self.target = qubits[1]
        self.angle = angle     

    def __str__(self) -> str:
        return "CRZ, control: " + str(self.control) +", target: " + str(self.target)

    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.crz(self.angle, qReg[mapping_bq[self.control]], qReg[mapping_bq[self.target]])

class SWAP(Gate):
    def __init__(self, qubits: list[int]):
        if len(qubits) != 2:
            print("SWAP gate should affect 2 qubit.")
            return
        super().__init__(qubits)

    def __str__(self) -> str:
        return "SWAP, control: " + str(self.control) +", target: " + str(self.target)

    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.swap(qReg[mapping_bq[self.slots[0]]], qReg[mapping_bq[self.slots[1]]])


# Util functions
def run_circuit(qc: QuantumCircuit, numShots: int=10, isPhysical: bool=False, hasNoise: bool=False):
    # Define which backend to use
    if isPhysical:
        service = QiskitRuntimeService(channel="ibm_quantum")
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
            try:
                qubit_set_list.remove(qubit_set)
            except Exception:
                pass
        qubit_set_list.append(union)

    # Freeze sets (so they can be used as index later)
    return [frozenset(x) for x in qubit_set_list]

# Circuit generators
def generate_physical_circuit(moves: list[Move], measurement_axes: set[Axis] = set([Axis.X, Axis.Y, Axis.Z])) -> tuple[QuantumCircuit, dict[int, int]]:
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
    
    regs: list[Register] = []
    qRegs: list[QuantumRegister] = []
    if Axis.X in measurement_axes:
        regs.append(qReg_x)
        regs.append(cReg_x)
        qRegs.append(qReg_x)
    if Axis.Y in measurement_axes:
        regs.append(qReg_y)
        regs.append(cReg_y)
        qRegs.append(qReg_y)
    if Axis.Z in measurement_axes:
        regs.append(qReg_z)
        regs.append(cReg_z)
        qRegs.append(qReg_z)

    # Add gates to the circuit
    qc = QuantumCircuit(*regs)
    for move in moves:
        move.gate.addToQc(qc, mapping_bq, qRegs)

    # Add measurements
    if Axis.X in measurement_axes:
        qc.h(qReg_x)
        qc.measure(qReg_x, cReg_x)
    if Axis.Y in measurement_axes:
        v = np.pi/np.sqrt(2)
        qc.rv(0, v, v, qReg_y)
        qc.measure(qReg_y, cReg_y)
    if Axis.Z in measurement_axes:
        qc.measure(qReg_z, cReg_z)

    return (qc, mapping_bq)

def generate_simulator_circuits(moves: list[Move]) -> tuple[list[list[QuantumCircuit]], dict[int, int]]:
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

    qcs_x, qcs_y, qcs_z = list(), list(), list()
    mapping_bq: dict[int, int] = dict()
    for move_sublist in moves_per_set.values():
        for qcs, axis in [(qcs_x, Axis.X), (qcs_y, Axis.Y), (qcs_z, Axis.Z)]:
            (qc, mapping_bq_temp) = generate_physical_circuit(move_sublist, set([axis]))
            qcs.append(qc)

            if axis == Axis.X:
                # Merge mappings (increase each value by number of keys in final mapping)
                offset: int = len(mapping_bq.keys())
                for k, v in mapping_bq_temp.items():
                    mapping_bq[k] = v + offset

        
    return ([qcs_x, qcs_y, qcs_z], mapping_bq)
        
def run_moves(moves: list[Move], numShots: int = 1, isPhysical: bool = False) -> tuple[tuple[str, str, str], dict[int, int]]:
    if isPhysical:
        (qc, mapping_bq) = generate_physical_circuit(moves)
        result = run_circuit(qc, numShots, False)
        data = result[0].data
        cReg_x = data.cReg_x.array
        cReg_y = data.cReg_y.array
        cReg_z = data.cReg_z.array
        return ((cReg_x, cReg_y, cReg_z), mapping_bq)
    else:
        (qcs, mapping_bq) = generate_simulator_circuits(moves)
        results = []
        for i in range(3):
            results.append([run_circuit(qc, numShots)[0].data for qc in qcs[i]])

        cReg_x = BitArray.concatenate_bits([i.cReg_x for i in results[0]]).get_bitstrings()
        cReg_y = BitArray.concatenate_bits([i.cReg_y for i in results[1]]).get_bitstrings()
        cReg_z = BitArray.concatenate_bits([i.cReg_z for i in results[2]]).get_bitstrings()
        return ((cReg_x, cReg_y, cReg_z), mapping_bq)