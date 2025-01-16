import tkinter
# requires gui package as main python file is outside of package
from gui.rotation_input import Rotation_input
from gui.CY_input import CY_input

class Input_panel():
    def __init__(self, parent, add_move):
        self.container = tkinter.Frame(parent, borderwidth=2, relief=tkinter.RIDGE)

        self.move_type_container = tkinter.Frame(self.container, borderwidth=2, relief=tkinter.RIDGE, padx=10,pady=5)
        self.move_type_container.grid(row=0,column=1)

        # attributes for the diffrent move inputs, starts with rotate input
        self.rotation_input = Rotation_input(self.move_type_container)
        self.control_y_input = CY_input(self.move_type_container)
        self.control_y_input.container.pack_forget() # hides CY input

        #switch move buttons
        self.move_select_container = tkinter.Frame(self.container, borderwidth=2, relief=tkinter.RIDGE)
        self.move_type: int = 0
        self.move_type_rotation = tkinter.Button(self.move_select_container, text='rotation move', command=self.show_rotation_input, state="disabled")
        self.move_type_rotation.grid(row=0, column=0, sticky="ew")

        self.move_type_control_y = tkinter.Button(self.move_select_container, text='CY move', command=self.show_control_y_input)
        self.move_type_control_y.grid(row=1, column=0, sticky="ew")

        self.move_select_container.grid(row=0,column=0, sticky="ns")

        #submit_move button
        self.submit_button = tkinter.Button(self.container, text='Play move', command=add_move)
        self.submit_button.grid(row=1, columnspan=2, sticky="ew")

    def clear_input(self):
        for child in self.move_type_container.winfo_children():
            child.pack_forget()
    
    def show_rotation_input(self):
        self.move_type_rotation["state"] = "disabled"
        self.move_type_control_y["state"] = "normal"
        self.clear_input()
        self.rotation_input.container.pack() # = Rotation_input(self.move_type_container)
        self.move_type = 0

    def show_control_y_input(self):
        self.move_type_control_y["state"] = "disabled"
        self.move_type_rotation["state"] = "normal"
        self.clear_input()
        self.control_y_input.container.pack() # = CY_input(self.move_type_container)
        self.move_type = 1

    def get_move(self):
        match self.move_type:
            case 0:
                return self.rotation_input.get_move()
            case 1:
                return self.control_y_input.get_move()