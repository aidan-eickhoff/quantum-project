import tkinter
import numpy as np
from input_panel import Input_panel
from bloch import BlochVisualizer

class BoardState():
    def __init__(self):
        self.board = np.zeros((7, 6))
        self.moves = []
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
    def collapse_event(self, target_turn: int|None = None) -> np.ndarray:
        if target_turn is None:
            target_turn = len(self.moves)
        if target_turn <= self.last_collapsed_move:
            print("Error, collapsing moves which are already collapsed")
            return
        new_board = self.collapse_moves(self.moves[self.last_collapsed_move:target_turn])
        self.last_collapsed_move = target_turn
        return new_board

class tkinterHandler():
    def __init__(self):
        self.main_window = tkinter.Tk()

        # create drawable canvas
        self.bloch_visualizer = BlochVisualizer(self.main_window) #constructor performs .pack()
        self.input_panel = Input_panel(self.main_window, None) #constructor performs .pack()

        self.bloch_visualizer.container.pack(side=tkinter.LEFT)
        self.input_panel.container.pack(side=tkinter.RIGHT)

        self.board_state: BoardState = BoardState()


    def show_window(self):
        self.main_window.mainloop()


if __name__ == "__main__":
    tkinter_handler = tkinterHandler()
    tkinter_handler.show_window()