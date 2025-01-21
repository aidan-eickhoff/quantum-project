from qiskit import *
from qiskit.circuit.quantumcircuit import *
from qiskit.primitives.containers import BitArray
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import *
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerOptions, SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import *

from abc import ABC, abstractmethod
import numpy as np

# Superclasses
class Move():
    def __init__(self, gate: Gate):
        self.gate: Gate = gate
        self.collapsed = False

    def __str__(self) -> str:
        return self.gate.__str__()

class Gate(ABC):
    def __init__(self, slots: list[int]):
        self.slots: list[int] = slots

    @abstractmethod
    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        pass

class Axis():
    def __init__(self):
        self.X = np.array([1,0,0])
        self.Y = np.array([0,1,0])
        self.Z = np.array([0,0,1])
        self.O = np.array([0,0,0])
Axis = Axis()

# Measurement & Collapse
class Meas(Gate):
    def __init__(self, axis: np.array, qubits: list[int]):
        super().__init__(qubits)
        self.axis = axis
        self.slots = qubits
    
    def __str__(self) -> str:
        return "Meas: Axis=(" + str(self.axis) + ")"

    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs:
            for t in self.slots:
                rot_axis = (Axis.Z + self.axis)
                rot_axis /= np.linalg.norm(rot_axis)
                qc.rv(*(rot_axis * np.pi), qReg[mapping_bq[t]]) # Add correct rotation to circuit
                qc.measure(qReg[mapping_bq[t]], ClassicalRegister(1, "useless"))
                qc.rv(*(rot_axis * np.pi), qReg[mapping_bq[t]]) # Reverse correct rotation to circuit

class Coll(Gate):
    def __init__(self, slots: list[int]):
        super().__init__(slots)
        self.slots = slots
    
    def __str__(self) -> str:
        x_pos = self.slots[0] % 7
        y_pos = int((self.slots[0] - x_pos) / 7)
        return "Collapse: Cell=(" + str(x_pos) +", " + str(y_pos) + ")"

    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        pass

# 1 qubit gates
class RX(Gate):
    def __init__(self, angle: float, qubits: list[int]):
        if len(qubits) != 1:
            print("RX gate should affect 1 qubit.")
            return
        super().__init__(qubits)
        self.angle: float = angle

    def __str__(self) -> str:
        x_pos = self.slots[0] % 7
        y_pos = int((self.slots[0] - x_pos) / 7)
        return "RX: Cell=(" + str(x_pos) + ", " + str(y_pos) + "), Angle=" + str(self.angle)

    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.rx(self.angle, qReg[mapping_bq[self.slots[0]]]) 

class RY(Gate):
    def __init__(self, angle: float, qubits: list[int]):
        if len(qubits) != 1:
            print("RY gate should affect 1 qubit.")
            return
        super().__init__(qubits)
        self.angle: float = angle

    def __str__(self):
        x_pos = self.slots[0] % 7
        y_pos = int((self.slots[0] - x_pos) / 7)
        return "RY: Cell=(" + str(x_pos) + ", " + str(y_pos) + "), Angle=" + str(self.angle)
    
    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.ry(self.angle, qReg[mapping_bq[self.slots[0]]]) 

class RZ(Gate):
    def __init__(self, angle: float, qubits: list[int]):
        if len(qubits) != 1:
            print("RZ gate should affect 1 qubit.")
            return
        super().__init__(qubits)
        self.angle: float = angle

    def __str__(self):
        x_pos = self.slots[0] % 7
        y_pos = int((self.slots[0] - x_pos) / 7)
        return "RZ: Cell=(" + str(x_pos) + ", " + str(y_pos) + "), Angle=" + str(self.angle)

    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.rz(self.angle, qReg[mapping_bq[self.slots[0]]]) 

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

    def __str__(self) -> str:
        x_pos = self.slots[0] % 7
        y_pos = int((self.slots[0] - x_pos) / 7)
        return "RV: Cell=(" + str(x_pos) + "," + str(y_pos) + "), Axis=(" + str(self.rot_axis) + "), Angle=" + str(self.rot_angle)
    
    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.rv(*(self.rot_axis * self.rot_angle), qReg[mapping_bq[self.slots[0]]])

class H(Gate):
    def __init__(self, qubits: list[int]):
        super().__init__(qubits)
        if len(qubits) != 1:
            print("H gate should affect 1 qubit.")
            return

    def __str__(self) -> str:
        return "H: " + str(self.slots[0])

    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.h(qReg[mapping_bq[self.slots[0]]])

# 2 qubit gates
class CX(Gate):
    def __init__(self, qubits: list[int]):
        if len(qubits) != 2:
            print("CX gate should affect 2 qubit.")
            return
        super().__init__(qubits)   

    def __str__(self) -> str:
        x_pos_control = self.slots[0] % 7
        y_pos_control = int((self.slots[0] - x_pos_control) / 7)
        x_pos_target = self.slots[1] % 7
        y_pos_target = int((self.slots[1] - x_pos_target) / 7)
        return "CX: Control=(" + str(x_pos_control) + ", " + str(y_pos_control) + "), Target=(" + str(x_pos_target) + ", " + str(y_pos_target) + ")"

    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.cx(qReg[mapping_bq[self.slots[0]]], qReg[mapping_bq[self.slots[1]]])

class CY(Gate):
    def __init__(self, qubits: list[int]):
        if len(qubits) != 2:
            print("CY gate should affect 2 qubit.")
            return
        super().__init__(qubits)   

    def __str__(self) -> str:
        x_pos_control = self.slots[0] % 7
        y_pos_control = int((self.slots[0] - x_pos_control) / 7)
        x_pos_target = self.slots[1] % 7
        y_pos_target = int((self.slots[1] - x_pos_target) / 7)
        return "CY: Control=(" + str(x_pos_control) + ", " + str(y_pos_control) + "), Target=(" + str(x_pos_target) + ", " + str(y_pos_target) + ")"
    
    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.cy(qReg[mapping_bq[self.slots[0]]], qReg[mapping_bq[self.slots[1]]])

class CZ(Gate):
    def __init__(self, qubits: list[int]):
        if len(qubits) != 2:
            print("CZ gate should affect 2 qubit.")
            return
        super().__init__(qubits)  

    def __str__(self) -> str:
        x_pos_control = self.slots[0] % 7
        y_pos_control = int((self.slots[0] - x_pos_control) / 7)
        x_pos_target = self.slots[1] % 7
        y_pos_target = int((self.slots[1] - x_pos_target) / 7)
        return "CZs: Control=(" + str(x_pos_control) + ", " + str(y_pos_control) + "), Target=(" + str(x_pos_target) + ", " + str(y_pos_target) + ")"

    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.cz(qReg[mapping_bq[self.slots[0]]], qReg[mapping_bq[self.slots[1]]])

class CRX(Gate):
    def __init__(self, angle, qubits: list[int]):
        if len(qubits) != 2:
            print("CRX gate should affect 2 qubit.")
            return
        super().__init__(qubits)
        self.angle = angle     

    def __str__(self) -> str:
        x_pos_control = self.slots[0] % 7
        y_pos_control = int((self.slots[0] - x_pos_control) / 7)
        x_pos_target = self.slots[1] % 7
        y_pos_target = int((self.slots[1] - x_pos_target) / 7)
        return "CRX: Control=(" + str(x_pos_control) + ", " + str(y_pos_control) + "), Target=(" + str(x_pos_target) + ", " + str(y_pos_target) + "), Angle=" + str(self.angle)

    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.crx(self.angle, qReg[mapping_bq[self.slots[0]]], qReg[mapping_bq[self.slots[1]]])

class CRY(Gate):
    def __init__(self, angle, qubits: list[int]):
        if len(qubits) != 2:
            print("CRY gate should affect 2 qubit.")
            return
        super().__init__(qubits)
        self.angle = angle     

    def __str__(self) -> str:
        x_pos_control = self.slots[0] % 7
        y_pos_control = int((self.slots[0] - x_pos_control) / 7)
        x_pos_target = self.slots[1] % 7
        y_pos_target = int((self.slots[1] - x_pos_target) / 7)
        return "CRY: Control=(" + str(x_pos_control) + ", " + str(y_pos_control) + "), Target=(" + str(x_pos_target) + ", " + str(y_pos_target) + "), Angle=" + str(self.angle)

    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.cry(self.angle, qReg[mapping_bq[self.slots[0]]], qReg[mapping_bq[self.slots[1]]])

class CRZ(Gate):
    def __init__(self, angle, qubits: list[int]):
        if len(qubits) != 2:
            print("CRZ gate should affect 2 qubit.")
            return
        super().__init__(qubits)
        self.angle = angle     

    def __str__(self) -> str:
        x_pos_control = self.slots[0] % 7
        y_pos_control = int((self.slots[0] - x_pos_control) / 7)
        x_pos_target = self.slots[1] % 7
        y_pos_target = int((self.slots[1] - x_pos_target) / 7)
        return "CRZ: Control=(" + str(x_pos_control) + ", " + str(y_pos_control) + "), Target=(" + str(x_pos_target) + ", " + str(y_pos_target) + "), Angle=" + str(self.angle)

    def addToQc(self, qc: QuantumCircuit, mapping_bq: dict[int, int], regs: list[QuantumRegister]):
        for qReg in regs: qc.crz(self.angle, qReg[mapping_bq[self.slots[0]]], qReg[mapping_bq[self.slots[1]]])

class SWAP(Gate):
    def __init__(self, qubits: list[int]):
        if len(qubits) != 2:
            print("SWAP gate should affect 2 qubit.")
            return
        super().__init__(qubits)

    def __str__(self) -> str:
        x_pos_control = self.slots[0] % 7
        y_pos_control = int((self.slots[0] - x_pos_control) / 7)
        x_pos_target = self.slots[1] % 7
        y_pos_target = int((self.slots[1] - x_pos_target) / 7)
        return "SWAP: Control=(" + str(x_pos_control) + ", " + str(y_pos_control) + "), Target=(" + str(x_pos_target) + ", " + str(y_pos_target) + ")"

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
        if len(move.gate.slots) < 2:
            continue

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
def generate_physical_circuit(moves: list[Move], measurement_axes: list[np.array] = [Axis.Z]) -> tuple[QuantumCircuit, dict[int, int]]:
    # Normalize and index measurement axes
    indexed_measurement_axes = lambda: enumerate([axis / np.linalg.norm(axis) for axis in measurement_axes])

    # Count number of necessary qubits (inefficiently)
    unique_qubits: set = set()
    for move in moves:
        for qubit in move.gate.slots:
            unique_qubits.add(qubit)

    _, mapping_bq = generate_mappings(unique_qubits)

    # Create quantum circuit
    q_num = len(unique_qubits)

    qRegs: list[QuantumRegister] = list()
    cRegs: list[ClassicalRegister] = list()
    
    # Create registers
    for index, axis in indexed_measurement_axes():
        qRegs.append(QuantumRegister(q_num, f"qReg_{index}"))
        cRegs.append(ClassicalRegister(q_num, f"cReg_{index}"))

    # Add gates to the circuit
    qc = QuantumCircuit(*qRegs, *cRegs, ClassicalRegister(1, "useless"))
    for move in moves:
        if move.collapsed:
            continue
        move.gate.addToQc(qc, mapping_bq, qRegs)

    # Add measurements
    for index, axis in indexed_measurement_axes():
        rot_axis = (Axis.Z + axis)
        rot_axis /= np.linalg.norm(rot_axis)
        qc.rv(*(rot_axis * np.pi), QuantumRegister(q_num, f"qReg_{index}")) # Add correct rotation to circuit
        qc.measure(QuantumRegister(q_num, f"qReg_{index}"), ClassicalRegister(q_num, f"cReg_{index}"))
        qc.rv(*(rot_axis * np.pi), QuantumRegister(q_num, f"qReg_{index}")) # Reverse correct rotation to circuit

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
                raise Exception("Not all qubits of a move were in the same set after seperation")

    qcs_x, qcs_y, qcs_z = list(), list(), list()
    mapping_bq: dict[int, int] = dict()
    for move_sublist in moves_per_set.values():
        for qcs, axis in [(qcs_x, Axis.X), (qcs_y, Axis.Y), (qcs_z, Axis.Z)]:
            (qc, mapping_bq_temp) = generate_physical_circuit(move_sublist, [axis])
            qcs.append(qc)

            if np.array_equal(axis, Axis.X):
                # Merge mappings (increase each value by number of keys in final mapping)
                offset: int = len(mapping_bq.keys())
                for k, v in mapping_bq_temp.items():
                    mapping_bq[k] = v + offset

        
    return ([qcs_x, qcs_y, qcs_z], mapping_bq)
        
def run_moves(moves: list[Move], numShots: int = 1, isPhysical: bool = False) -> tuple[tuple[BitArray, BitArray, BitArray], dict[int, int]]:
    if isPhysical:
        (qc, mapping_bq) = generate_physical_circuit(moves, [Axis.X, Axis.Y, Axis.Z])
        result = run_circuit(qc, numShots, False) # Change this False to True to run on IBM
        data = result[0].data
        cReg_x = data.cReg_0
        cReg_y = data.cReg_1
        cReg_z = data.cReg_2
        return ((cReg_x, cReg_y, cReg_z), mapping_bq)
    else:
        (qcs, mapping_bq) = generate_simulator_circuits(moves)
        results = list()

        if qcs == [[], [], []]:
            return tuple([BitArray([]) for i in range(3)], mapping_bq)

        # Add a list of all results for each axis to `results` 
        for i in range(3):
            results.append([run_circuit(qc, numShots)[0].data for qc in qcs[i]])

        return (tuple([BitArray.concatenate_bits([res.cReg_0 for res in axisResults]) for axisResults in results]), mapping_bq)