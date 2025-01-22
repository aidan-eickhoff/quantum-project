import tkinter
import numpy as np
from gui.input_panel import Input_panel
from bloch import BlochVisualizer
from recent_moves import Recent_moves_list
import circuit_generation
from qiskit.primitives.containers import BitArray
import platform

class BoardState():
    def __init__(self):
        self.board = np.zeros((7, 6))
        self.moves: list[circuit_generation.Move] = list()
        self.last_collapsed_move = 0
        self.total_move_number = 0
        self.red_turn = True

    # add a classical piece to a column in a board_state (self.board if None is supplied)
    def add_to_col(self, col: int, is_red:bool, curr_board: np.ndarray | None = None) -> np.ndarray:
        if curr_board is None:
            curr_board = self.board
        for row in range(6):
            if curr_board[col][5 - row] == 0.:
                # 1 in array represents red, 2 represents yellow
                curr_board[col][5 - row] = 1 if is_red else 2
                self.check_win()
                break
            if row == 5:
                print("no space")
        return curr_board
    

    # check for a winning move on the current board
    def check_win(self):
        for col in range(0, 7):
            for row in range(0, 6):
                if row < 3 and self.board[col][row] == self.board[col][row + 1] == self.board[col][row + 2] == self.board[col][row + 3] != 0:
                    print("winner " + ("red" if self.board[col][row] == 1 else "yellow"))
                if col < 4 and self.board[col][row] == self.board[col + 1][row] == self.board[col + 2][row] == self.board[col + 3][row] != 0:
                    print("winner " + ("red" if self.board[col][row] == 1 else "yellow"))
                if row < 3 and col < 4 and self.board[col][row] == self.board[col + 1][row + 1] == self.board[col + 2][row + 2] == self.board[col + 3][row + 3] != 0:
                    print("winner " + ("red" if self.board[col][row] == 1 else "yellow"))
                if row < 3 and col > 2 and self.board[col][row] == self.board[col - 1][row + 1] == self.board[col - 2][row + 2] == self.board[col - 3][row + 3] != 0:
                    print("winner " + ("red" if self.board[col][row] == 1 else "yellow"))


    # called to collapse the board up to a target turn -- returns the updated board
    def collapse_event(self, target_turn: int|None = None, isPhysical = False) -> tuple[tuple[list[int], list[int], list[int]], dict[int, int]]:
        if target_turn is None:
            target_turn = len(self.moves)
        if target_turn <= self.last_collapsed_move:
            raise Exception("Error, collapsing moves which are already collapsed")
        return circuit_generation.run_moves(self.moves[self.last_collapsed_move: target_turn], 1000, isPhysical=isPhysical)

class tkinterHandler():
    def __init__(self):
        self.main_window = tkinter.Tk()
        # fit the window to the screen -- I <3 platform dependent code!
        if platform.system() == 'Linux':
            self.main_window.attributes('-zoomed', True)
            self.main_window.update()
        else:
            self.main_window.state('zoomed')
            
        # create drawable canvas
        self.bloch_visualizer = BlochVisualizer(self.main_window)
        self.input_panel = Input_panel(self.main_window, self.add_move, self.undo_move)
        self.recent_moves_list = Recent_moves_list(self.main_window)

        self.input_panel.container.grid(column=0, row=0, padx= 10)
        self.recent_moves_list.container.grid(column=0, row=1, padx=10, sticky="news")
        self.bloch_visualizer.container.grid(column=1,row=0, rowspan=2)

        self.board_state: BoardState = BoardState()


        self.vector_colors = [
            "#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#A133FF", "#33FFF5", "#F5FF33",
            "#FF8C33", "#8CFF33", "#338CFF", "#FF338C", "#8C33FF", "#33FF8C", "#FF5733",
            "#33FFDD", "#DD33FF", "#FFDD33", "#33A1FF", "#A1FF33", "#FF33DD", "#33FFA1",
            "#FFD733", "#D733FF", "#33FFD7", "#5733FF", "#33D7FF", "#FF33A8", "#A833FF",
            "#FFA833", "#33FFA8", "#FF3357", "#57FF33", "#A157FF", "#57FFA1", "#33A157",
            "#FF7F50", "#6495ED", "#DC143C", "#00FA9A", "#FFD700", "#8A2BE2", "#20B2AA"
        ]

    def show_window(self):
        self.main_window.mainloop()


    # submit button click calls this method
    def add_move(self):
        # Get move and add it to administration
        m: circuit_generation.Move = self.input_panel.get_move()
        self.board_state.moves.append(m)
        self.recent_moves_list.add_move(m)

        # Mark all qubits in this move as "touched"
        for qubit in m.gate.slots:
            col = qubit % 7
            row = int((qubit - col) / 7)
            b = self.board_state.board
            if b[col][row] > 0:
                continue
            b[col][row] = -1


        # We will be collapsing one qubit and all of its entangled partners, if this is a collapse move
        if isinstance(m.gate, circuit_generation.Coll):
            # Get measurements to collapse with
            (measurements, mapping_bq) = self.board_state.collapse_event(isPhysical=False)
            qubit_sets = circuit_generation.generate_seperation(self.board_state.moves)

            # Find the set that was affected by our collapse move
            for qubit_set in qubit_sets:
                if not all(s in qubit_set for s in m.gate.slots):
                    continue
                # Collapse all qubits in this set according to their measurements
                for qubit in qubit_set:
                    # Find last X and Z measurement, we use these for determining fullness and color of a cell
                    measX = int(measurements[0].get_bitstrings()[0][-1 - mapping_bq[qubit]])
                    measZ = int(measurements[2].get_bitstrings()[0][-1 - mapping_bq[qubit]])
                    
                    col = qubit % 7
                    row = int((qubit - col) / 7)

                    # If a cell is already filled, don't empty or recolor it
                    if self.board_state.board[col][row] > 0:
                        continue

                    # If cell full, red
                    if measZ == 1 and measX == 0:
                        self.board_state.board[col][row] = 1
                    # Elif cell full, yellow
                    elif measZ == 1 and measX == 1:
                        self.board_state.board[col][row] = 2
                    # Else cell empty
                    else: 
                        self.board_state.board[col][row] = 0
                    
                # Define a mapping to apply later
                mapping = [i for i in range(42)]
                # Apply gravity
                for col in range(7):
                    lowest = 5
                    # Find the lowest free spot
                    for row in range(6):
                        if self.board_state.board[col][row] == 0:
                            lowest = row
                            break
                    # Fill free spots bottom up
                    for row in range(lowest,6):
                        if self.board_state.board[col][row] == 0:
                            continue
                        self.board_state.board[col][lowest] = self.board_state.board[col][row]
                        mapping[7 * row + col] = 7 * lowest + col
                        self.board_state.board[col][row] = 0
                        self.bloch_visualizer.set_color(col, row, 'g')
                        lowest += 1
                # Apply coloring
                for col in range(7):
                    for row in range(6):
                        # if self.board_state.board
                        if self.board_state.board[col][row] == 0:
                            self.bloch_visualizer.set_vector(col, row, np.array([0, 0, 1.1]))
                        if self.board_state.board[col][row] <= 0:
                            continue
                        self.bloch_visualizer.set_collapsed_color(col, row, self.board_state.board[col][row] == 1)

                # Apply mapping
                for move in self.board_state.moves:
                    if all(s in qubit_set for s in move.gate.slots):
                        move.collapsed = True

                    for i,q in enumerate(move.gate.slots):
                        move.gate.slots[i] = mapping[q]
                            
        # Rerender the board
        self.update_board(*self.board_state.collapse_event(isPhysical=False))

    def undo_move(self):
        self.board_state.moves.pop()
        self.recent_moves_list.remove_last()
        self.update_board(*self.board_state.collapse_event(isPhysical=False))

    def update_board(self, measurements: tuple[BitArray, BitArray, BitArray], mapping_bq: dict[int, int]):
        qubit_sets: list[frozenset[int]] = circuit_generation.generate_seperation(self.board_state.moves)
        for col in range(7):
            for row in range(6):
                qb_num = 7 * row + col
                if qb_num not in mapping_bq.keys():
                    continue
                
                # takes a length 3 np array representing a vector. We want to get the mean value of all the measurements in a certain axis
                self.bloch_visualizer.set_vector(col, row, np.array([\
                    # mean
                    np.mean(
                        # np array from python map object to allow for nice slicing & casting
                        np.array(list(map(
                            # map the bitstrings to arrays of characters using the list() method
                            list, measurements[i].get_bitstrings())))
                            # we get a 2d array out. the first dimension is the shot #, the second dimension is the result for qubit #n. 
                            # since we want the average we need to keep all shots while selecting just a single qubit.
                            # mapping_bq[qb_num] tells the virtual qubit number from the position on the board calculated above.
                            [:,-1 - mapping_bq[qb_num]]
                            # cast from char to float and convert digital measurements to correct locations on the bloch sphere
                            .astype(np.float64) * -2. + 1) for i in range(3)
                ]))
                for i, qb_set in enumerate(qubit_sets):
                    if qb_num in qb_set:
                        self.bloch_visualizer.set_color(col, row, self.vector_colors[i])


if __name__ == "__main__":
    tkinter_handler = tkinterHandler()
    tkinter_handler.show_window()