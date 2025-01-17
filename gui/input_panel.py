from enum import Enum
import tkinter
# requires gui package as main python file is outside of package
from gui.rotation_input import Rotation_input
from gui.CY_input import CY_input
from gui.measure_input import Measure_Input

class MoveType(Enum):
    RV = 'rv'
    CY = 'cy'
    MEAS = 'meas'

class Input_panel():
    def __init__(self, parent, add_move):
        self.container = tkinter.Frame(parent, borderwidth=2, relief=tkinter.RIDGE)

        self.move_type_container = tkinter.Frame(self.container, borderwidth=2, relief=tkinter.RIDGE, padx=10,pady=5)
        self.move_type_container.grid(row=0,column=1)

        # attributes for the diffrent move inputs, starts with rotate input
        self.rotation_input = Rotation_input(self.move_type_container)
        self.control_y_input = CY_input(self.move_type_container)
        self.control_y_input.container.pack_forget() # hides CY input
        self.measure_input = Measure_Input(self.move_type_container)
        self.measure_input.container.pack_forget()

        #switch move buttons
        self.move_select_container = tkinter.Frame(self.container, borderwidth=2, relief=tkinter.RIDGE)
        self.move_type: MoveType = MoveType.RV
        self.move_type_select_buttons = list()

        self.move_type_rotation = tkinter.Button(self.move_select_container, text='rotation move', command=lambda: self.show_type_input(MoveType.RV), state="disabled")
        self.move_type_rotation.grid(row=0, column=0, sticky="ew")
        self.move_type_select_buttons.append(self.move_type_rotation)

        self.move_type_control_y = tkinter.Button(self.move_select_container, text='CY move', command=lambda: self.show_type_input(MoveType.CY))
        self.move_type_control_y.grid(row=1, column=0, sticky="ew")
        self.move_type_select_buttons.append(self.move_type_control_y)

        self.move_type_measure = tkinter.Button(self.move_select_container, text='Measure move', command=lambda: self.show_type_input(MoveType.MEAS))
        self.move_type_measure.grid(row=2, column=0, sticky="ew")
        self.move_type_select_buttons.append(self.move_type_measure)

        self.move_select_container.grid(row=0, column=0, sticky="ns")

        #submit_move button
        self.submit_button = tkinter.Button(self.container, text='Play move', command=add_move)
        self.submit_button.grid(row=1, columnspan=2, sticky="ew")

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
            case MoveType.CY:
                self.move_type_control_y["state"] = "disabled"
                self.control_y_input.container.pack() # = CY_input(self.move_type_container)
            case MoveType.MEAS:
                self.move_type_measure["state"] = "disabled"
                self.measure_input.container.pack()


    def get_move(self):
        match self.move_type:
            case MoveType.RV:
                return self.rotation_input.get_move()
            case MoveType.CY:
                return self.control_y_input.get_move()
            case MoveType.MEAS:
                return self.measure_input.get_move()