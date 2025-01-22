from enum import Enum
import tkinter
# requires gui package as main python file is outside of package
from gui.collapse_input import Collapse_input
from gui.rotation_input import Rotation_input
from gui.CRY_input import CRY_input
from gui.measure_input import Measure_input
from gui.swap_input import Swap_input

class MoveType(Enum):
    RV = 'rv'
    CRY = 'cry'
    SWAP = 'swap'
    MEAS = 'meas'
    COLLAPSE = 'collapse'

class Input_panel():
    def __init__(self, parent, add_move, undo_move, rerun):
        self.container = tkinter.Frame(parent, borderwidth=2, relief=tkinter.RIDGE)

        self.move_type_container = tkinter.Frame(self.container, borderwidth=2, relief=tkinter.RIDGE, padx=10, pady=5)
        self.move_type_container.grid(row=0,column=1, sticky = "ns")

        # attributes for the diffrent move inputs, starts with rotate input
        self.rotation_input = Rotation_input(self.move_type_container)
        self.control_y_input = CRY_input(self.move_type_container)
        self.control_y_input.container.pack_forget() # hides CY input
        self.measure_input = Measure_input(self.move_type_container)
        self.measure_input.container.pack_forget()
        self.collapse_input = Collapse_input(self.move_type_container)
        self.collapse_input.container.pack_forget()
        self.swap_input = Swap_input(self.move_type_container)
        self.swap_input.container.pack_forget()

        #switch move buttons
        self.move_select_container = tkinter.Frame(self.container, borderwidth=2, relief=tkinter.RIDGE)
        self.move_type: MoveType = MoveType.RV
        self.move_type_select_buttons = list()

        self.move_type_rotation = tkinter.Button(self.move_select_container, text='rotation move', command=lambda: self.show_type_input(MoveType.RV), state="disabled")
        self.move_type_rotation.grid(row=0, column=0, sticky="ew")
        self.move_type_select_buttons.append(self.move_type_rotation)

        self.move_type_control_y = tkinter.Button(self.move_select_container, text='CRY move', command=lambda: self.show_type_input(MoveType.CRY))
        self.move_type_control_y.grid(row=1, column=0, sticky="ew")
        self.move_type_select_buttons.append(self.move_type_control_y)
        
        self.move_type_swap = tkinter.Button(self.move_select_container, text='Swap', command=lambda: self.show_type_input(MoveType.SWAP))
        self.move_type_swap.grid(row=2, column=0, sticky="ew")
        self.move_type_select_buttons.append(self.move_type_swap)

        self.move_type_measure = tkinter.Button(self.move_select_container, text='Measure move', command=lambda: self.show_type_input(MoveType.MEAS))
        self.move_type_measure.grid(row=3, column=0, sticky="ew")
        self.move_type_select_buttons.append(self.move_type_measure)

        self.move_type_collapse = tkinter.Button(self.move_select_container, text='Collapse', command=lambda: self.show_type_input(MoveType.COLLAPSE))
        self.move_type_collapse.grid(row=4, column=0, sticky="ew")
        self.move_type_select_buttons.append(self.move_type_collapse)

        self.move_select_container.grid(row=0, column=0, sticky="ns")

        #submit_move button
        self.submit_button = tkinter.Button(self.container, text='Play move', command=add_move)
        self.submit_button.grid(row=1, columnspan=2, sticky="ew")

        # undo move button
        self.undo_button = tkinter.Button(self.container, text="Undo last move", command=undo_move)
        self.undo_button.grid(row=2, columnspan=2, sticky="ew")

        self.rerun_button = tkinter.Button(self.container, text="Rerun all moves", command=rerun)
        self.rerun_button.grid(row=3, columnspan=2, sticky="ew")

    def clear_input(self):
        for child in self.move_type_container.winfo_children():
            child.pack_forget()
    
    def show_type_input(self, moveType: MoveType):
        for b in self.move_type_select_buttons:
            b["state"] = "normal"

        self.move_type = moveType
        self.clear_input()

        match moveType:
            case MoveType.RV:
                self.move_type_rotation["state"] = "disabled"
                self.rotation_input.container.pack() # = Rotation_input(self.move_type_container)
            case MoveType.CRY:
                self.move_type_control_y["state"] = "disabled"
                self.control_y_input.container.pack() # = CY_input(self.move_type_container)
            case MoveType.SWAP:
                self.move_type_swap["state"] = "disabled"
                self.swap_input.container.pack()
            case MoveType.MEAS:
                self.move_type_measure["state"] = "disabled"
                self.measure_input.container.pack()
            case MoveType.COLLAPSE:
                self.move_type_collapse["state"] = "disabled"
                self.collapse_input.container.pack()

    def get_move(self):
        match self.move_type:
            case MoveType.RV:
                return self.rotation_input.get_move()
            case MoveType.CRY:
                return self.control_y_input.get_move()
            case MoveType.SWAP:
                return self.swap_input.get_move()
            case MoveType.MEAS:
                return self.measure_input.get_move()
            case MoveType.COLLAPSE:
                return self.collapse_input.get_move()