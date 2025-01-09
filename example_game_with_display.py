import copy

import tkinter
import numpy as np
import math

from itertools import product

m = tkinter.Tk()
m.resizable(False, False)

cw, ch = 1280, 720

w = tkinter.Canvas(m, width=cw, height=ch)
w.create_rectangle(0, 0, cw, ch, fill="#faa", outline="#faa")

start_grid = (cw / 2 - (ch * 7 / 12))
grid_width =  ch / 6

red_turn = True

# board = np.zeros((7,6))
moves = []


def get_pos(col, row):
    return (start_grid + col * grid_width + 5, 0 + row * grid_width + 5)

for k in range(0, 7):
    for j in range(0, 6):
        offx, offy = get_pos(k, j)
        w.create_oval(offx, offy, offx + grid_width - 10, offy + grid_width - 10, fill="#fff", outline="#faa")

def updateCanvas()->None:
    # draw background
    for k in range(0, 7):
        for j in range(0, 6):
            offx, offy = get_pos(k, j)
            w.create_oval(offx, offy, offx + grid_width - 10, offy + grid_width - 10, fill="#fff", outline="#faa")
    # draw expectation values
    current_boards:list[Board] = flatten_nested_list(master_board.traverse(i+1))
    # print("I have found the following boards to use for displaying")
    # for board in current_boards:
    #     print("probability", board.get_total_probability())
    #     board.draw()
    #     print("--------------------")
    # print("Making frame")
    columns = [0,1,2,3,4,5,6]
    rows = [0,1,2,3,4,5]
    for row,column in product(rows,columns):
        expectation_red = 0
        expectation_yellow = 0
        for board in current_boards:
            chip:Chip | None = board.board[column][row]
            if chip is None:
                pass
            else:
                if chip.color == "R":
                     expectation_red += board.get_total_probability()
                else: # the chip is yellow
                    expectation_yellow+=board.get_total_probability()
        offx, offy = get_pos(column,row)
        # change colour based on the probability of each color
        start_angle = 0
        redangle = expectation_red * 359 # 359 looks better than 360
        yellow_angle = expectation_yellow * 359
        # yellow_final = redangle + yellow_angle
        w.create_arc(offx,offy, offx + grid_width - 10, offy + grid_width - 10, fill="#f00", outline="#faa",start=0,extent=redangle,style=tkinter.PIESLICE)
    
        w.create_arc(offx,offy, offx + grid_width - 10, offy + grid_width - 10, fill="#ff0", outline="#faa",start=redangle,extent=yellow_angle,style=tkinter.PIESLICE)


def on_place_click(event):
    global i
    do_turn()
    updateCanvas()
    i+=1

def check_win():
    global board
    for col in range(0, 7):
        for row in range(0, 6):
            if row < 3 and board[col][row] == board[col][row + 1] == board[col][row + 2] == board[col][row + 3] != 0:
                print("winner " + ("red" if board[col][row] == 1 else "yellow"))
            if col < 4 and board[col][row] == board[col + 1][row] == board[col + 2][row] == board[col + 3][row] != 0:
                print("winner " + ("red" if board[col][row] == 1 else "yellow"))
            if row < 3 and col < 4 and board[col][row] == board[col + 1][row + 1] == board[col + 2][row + 2] == board[col + 3][row + 3] != 0:
                print("winner " + ("red" if board[col][row] == 1 else "yellow"))
            if row < 3 and col > 2 and board[col][row] == board[col - 1][row + 1] == board[col - 2][row + 2] == board[col - 3][row + 3] != 0:
                print("winner " + ("red" if board[col][row] == 1 else "yellow"))
            


def add_move():
    pass
    # moves.append({something based on uyser input})


w.pack()
m.bind("<Button-1>", on_place_click)

# end of canvas stuff


R1 = {"type": "superposition",
      "distribution": [0 , 0 , 0.34, 0.33, 0.33, 0 , 0] # distribution of the superposition. THere is a 33% chance of being in column 3, 4, or 5
      }
Y1 = {"type": "superposition",
      "distribution": [0 , 0 , 0   , 0.5 , 0.5 , 0 , 0] # distribution of the superposition. THere is a 50% chance of being in column 4 or 5
      }
R2 = {"type": "entanglement",
      "entangled with": "Y1", # entanglement type needs a move to entangle with. This move HAS to be a superposition move
      "distribution": [None,None,None,4,3,None,None] # distribution of the entanglement.
      # If the superposition move is in column 4, then this move will be in column 5.
      # If the superposition move is in column 5, then this move will be in column 4
      # None means that it is not valid. The superposition move cannot be in column 3 or 6 for example, it has a zero probability of being there
      }
Y2 = {"type": "superposition", 
      "distribution": [0 , 0 , 1, 0,0,0,0] # this is a "classical" move
    }
CollapseR1 = {"type": "collapse",
              "Final position": 4, # this is the index of the final position of the chip
              "collapse turn": "R1"
    }
R3 = {"type": "superposition",
        "distribution": [0 , 0 , 0.5, 0.5, 0 , 0 , 0] # distribution of the superposition. THere is a 50% chance of being in column 3 or 4
        }
CollapseY1 = {"type": "collapse",
                "Final position": 4, # this is the index of the final position of the chip
                "collapse turn": "Y1"
    }
Y3 = {"type": "entanglement",
        "entangled with": "R3", # entanglement type needs a move to entangle with. This move HAS to be a superposition move
        "distribution": [None,None,3,2,None,None,None] # distribution of the entanglement.
        }
R4 = {"type": "superposition",
        "distribution": [0 , 0 , 0 , 0.5, 0 , 0.5 , 0]
        }
Y4 = {"type": "entanglement",
        "entangled with": "R4", # entanglement type needs a move to entangle with. This move HAS to be a superposition move
        "distribution": [None,None,None,None,3,5,None] # distribution of the entanglement.
        }
CollapseR3 = {"type": "collapse",
                "Final position": 3, # this is the index of the final position of the chip
                "collapse turn": "R3"
}
R5 = {"type": "superposition",
        "distribution": [0 , 0 , 1 , 0 , 0 , 0 , 0]
        }
Y5 = {"type": "entanglement",
        "entangled with": "R4",
        "distribution": [None,None,None,3,None,None,5] # distribution of the entanglement.
        }
CollapseR4 = {"type": "collapse",
                "Final position": 3, # this is the index of the final position of the chip
                "collapse turn": "R4"
}
R6 = {"type": "superposition",
        "distribution": [0 , 0.2 , 0.2 , 0.2 , 0.2 , 0.2 , 0]
        }
Y6 = {"type": "entanglement",
        "entangled with": "R6",
        "distribution": [None,None,5,None,[2,3],None,[1,4]] # distribution of the entanglement.
        # there should go a chip in index 2 if [5] is satisfied, that is, if the superposition move is in column with index 5
        }
R7 = {"type": "entanglement",
        "entangled with": "R6",
        "distribution": [None,[1,4],None,None,[2,3],5,None] # distribution of the entanglement.
        }
Y7 = {"type": "superposition",
        "distribution": [0 , 0 , 1 , 0, 0 , 0 , 0]
        }
CollapseR6 = {"type": "collapse",
                "Final position": 2, # this is the index of the final position of the chip
                "collapse turn": "R6"
}
R8 = {"type": "superposition",
        "distribution": [0 , 1 , 0 , 0 , 0 , 0 , 0]
        }
Y8 = {"type": "superposition",
        "distribution": [0 , 0 , 0 , 1 , 0 , 0 , 0]
        }
R9 = {"type": "superposition",
        "distribution": [0 , 1 , 0 , 0 , 0 , 0 , 0]
        }
Y9 = {"type": "superposition",
        "distribution": [0 , 0, 1 , 0 , 0 , 0 , 0]
        }
R10 = {"type": "superposition",
        "distribution": [0 , 1 , 0 , 0 , 0 , 0 , 0]
        }
Y10 = {"type": "superposition",
        "distribution": [0 , 1 , 0 , 0 , 0 , 0 , 0]
        }
R11 = {"type": "superposition",
        "distribution": [1 , 0 , 0 , 0 , 0 , 0 , 0]
        }
Y11 = {"type": "superposition",
        "distribution": [0 , 0 , 0 , 0 , 0 , 1 , 0]
        }
R12 = {"type": "superposition",
        "distribution": [0.5 , 0 , 0 , 0 , 0 , 0.5 , 0]
        }
Y12 = {"type": "entanglement",
        "entangled with": "R12",
        "distribution": [0,None,None,None,None,5,None]
        }
R13 = {"type": "superposition",
        "distribution": [1 , 0 , 0 , 0 , 0 , 0 , 0]
        }
CollapseR12 = {"type": "collapse", 
                "Final position": 5, # this is the index of the final position of the chip
                "collapse turn": "R12"
}

class Chip:
    def __init__(self, color:str, move:str):
        self.color = color # "R" or "Y"
        self.move = move # bijvoorbeed R1 of Y3 of R6


    def __str__(self):
        return self.color
    
class Board:
    def __init__(self,parent = None)->None:
            self.parent:Board | None = parent
            self.board = [[None for height in range(6)] for j in range(7)] # j == column number
            self.probability:float = 1.0 # the initial board has a probability of 1
                # maybe have children boards? so that we can backtrack?
            self.child_boards = []
            self.layer:int = 0
    def make_child(self, probability:float):
        child_board:Board = Board(parent = self)
        child_board.board = copy.deepcopy(self.board) # maybe we should make a .copy()????? I have made a copy but mutatiing this value still mutates the parent board as well. Now copy.deepcopy() solves it using magic i guess
        child_board.layer = self.layer+1
        self.child_boards.append(child_board)
        child_board.probability = probability
        return child_board # pass by reference, so modifyable
    
    def kill_children(self): # i like to kill children (for legal reasons, this is a joke)
        # we dont really have a deconstructor. welcome to the future. we dont have to micromanage memory like 70s peasents
        for child in self.child_boards:
            child.kill_children()
        self.child_boards = []

    def traverse(self,depth:int)->list:
        # recusively traverse. exponential
        if depth == 0:
            return [self] # I think this is why i sometimes have [[elem],[elem]] instead of [elem,elem]
        return [child.traverse(depth-1) for child in self.child_boards] # does this turn it into a proper list or maybe into a list with other lists inside it? maybe unpack (*) before child.traverse

    def list_all_children_and_self(self,list_to_add_to:list)->list:
        for child in self.child_boards:
            child.list_all_children_and_self(list_to_add_to)
        list_to_add_to.append(self)
        return list_to_add_to
    
    def get_total_probability(self)->float:
        if not self.parent == None:
            return self.probability * self.parent.get_total_probability()
        else:
            return self.probability
        
    def draw(self):
    # Iterate through rows in reverse (to display the board bottom-up)
        for height in range(5, -1, -1):
            row = ""
            for col in range(7):
                cell = self.board[col][height]
                if cell is None:
                    row += " O "  # Empty cell
                else:
                    row += f" {cell.color}{cell.move[1:]}"  # Display move like R1 or Y1
            print(row)
        print(" 0  1  2  3  4  5  6 ")  # Column numbers for reference

    def remove_child(self, child):
        prob = child.probability
        probability_multiplication_factor = 1/(1-prob)
        self.child_boards.remove(child)
        if not len(self.child_boards) == 0:
            # add a bit of probability to all options
            for children in self.child_boards:
                 children.probability *= probability_multiplication_factor

    

# this function is here because i am not good at programming, so i got chatgpt to write this for me
def flatten_nested_list(nested_list):
    result = []
    for elem in nested_list:
        if isinstance(elem, list):  # Check if the element is a list
            result.extend(flatten_nested_list(elem))  # Recursively flatten it
        else:
            result.append(elem)  # Add non-list elements directly
    return result


events = [R1,Y1,R2,Y2,CollapseR1,R3,CollapseY1,Y3,R4,Y4,CollapseR3,R5,Y5,CollapseR4,R6,Y6,R7,Y7,CollapseR6,R8,Y8,R9,Y9,R10,Y10,R11,Y11,R12,Y12,R13,CollapseR12]
global collapses
collapses = 0
master_board = Board()
superposition_moves = {} # we need to keep track of which superposition moves have been played. So we know how to entangle
i = 0
print("[DEBUG] 1")
    

def do_turn():
        global collapses
        print("[DEBUG] superposition moves observed: ", superposition_moves)
        event:dict = events[i]
        current_possible_boards:list[Board] = master_board.traverse(depth=i)
        current_possible_boards = flatten_nested_list(current_possible_boards)
        print("[DEBUG] number of current possible boards: ", len(current_possible_boards))
        if event["type"] == "superposition":
            
            # update superposition moves
            color = "Y"
            if (i-collapses)%2==0: color = "R"
            move = color + str(((i-collapses)//2)+1)
            superposition_moves.update({move: i})

            distribution:list[float] = event["distribution"]
            for current_board in current_possible_boards:
                for j in range(7):
                        if distribution[j] == 0:
                            continue # continue for next of this for loop
                        # determine to which height the chip will fall
                        height:int = 0 # array indices must be ints
                        while height<=6:
                            if current_board.board[j][height] == None:
                                break
                            else:
                                height += 1
                        # we have found the correct spot. Now we add the chip in a child
                        child_board = current_board.make_child(probability=distribution[j])
                        color = "Y"
                        if (i-collapses)%2==0: color = "R"
                        move = color + str(((i-collapses)//2)+1)
                        child_board.board[j][height] = Chip(color,move)
        elif event["type"] == "entanglement":
        # an example:
# R2 = {"type": "entanglement",
#       "entangled with": "Y1", # entanglement type needs a move to entangle with. This move HAS to be a superposition move
#       "distribution": [None,None,None,4,3,None,None] # distribution of the entanglement.
#       # If the superposition move is in column 4, then this move will be in column 5.
#       # If the superposition move is in column 5, then this move will be in column 4
#       # None means that it is not valid. The superposition move cannot be in column 3 or 6 for example, it has a zero probability of being there
# }
            old_move = event["entangled with"] # example; Y1
            old_move_number:int = superposition_moves[old_move] # example 1
            distribution = event["distribution"] # example [0,0,0,4,3,0,0]
            for j in range(7):
                if distribution[j] is None:
                    continue
                # we want to place a chip of our color at this column (still have to find height) IF the chip on the old turn ended up going into slot distribution[j]
                # first grep aka grab all boards at level old_move_number
                old_move_states = master_board.traverse(depth = old_move_number+1) # optimisation idea; we can cache this; off by errer hahahahahaahah 
                old_move_states = flatten_nested_list(old_move_states)

                # filter for the boardstates where the chip actually ended up in the specified column
                column_to_checks = distribution[j] # might be a list of multiple numbers

                if type(column_to_checks) != list:
                     column_to_checks = [column_to_checks]

                for column_to_check in column_to_checks:
                    for state in old_move_states:
                        # print("[DEBUG] Currently analysing board " , state.draw())
                        # print(f"[DEBUG] Hoping to find {old_move} at index {column_to_check}")
                        # get height
                        height = 5
                        while height >= 0:
                                if state.board[column_to_check][height] is not None:
                                        break
                                height -= 1
                        if height == -1:
                                # print("[DEBUG] faillure 1")
                                continue
                        # we found the top chip in this column of this board state, lets check if it's from this turn
                        coin:Chip = state.board[column_to_check][height] 
                        if not coin.move == old_move:
                             #faillure
                        #      print("[DEBUG] faillure 2")
                             continue
                        
                        # print("[DEBUG] succes")
                        # then only do the following for the boardstates where the chip actually ended up in the specified column
                        # just go to all available ends from this point on forward
                        offset = i - old_move_number # this is how many steps along the tree we need to take to get to where we are NOW, like now now ( at i )

                        # we have all satisfactory old boards in old_boards_filtered:list[Board]
                        # we need to fast-foward them all to where we are now
                        # They could have multiple branches
                        fastforwarded_boards = []
                        fastforwarded_boards.append(state.traverse(offset - 1))

                        # what if the player tries to react to a move that is never played? or if a player doest make a reaction to a move that is played? NOTE NO input validation
                        
                                
                        #fastforwarded_bopards might have a structure like [elem,[elem,[elem]]]. Transform it to [elem,elem,elem]
                        current_boards = flatten_nested_list(fastforwarded_boards)
                        # play the chip at index j (find the height first, at the start of this step)
                        for current_board in current_boards:
                        # find height
                                height:int = 0 # array indices must be ints
                                while height<=6:
                                        if current_board.board[j][height] == None:
                                                break
                                        else:
                                                height += 1
                                # we have found the correct spot. Now we add the chip in a child
                                child_board = current_board.make_child(probability=1)
                                color = "Y"
                                if (i-collapses)%2==0: color = "R"
                                move = color + str(((i-collapses)//2)+1)
                                child_board.board[j][height] = Chip(color,move)
                                # print("[DEBUG] Added child with board  ")
                                # print(child_board.draw())

        elif event["type"] == "collapse":
            collapses+=1
            # example
#CollapseR1 = {"type": "collapse",
#              "Final position": 4, # this is the index of the final position of the chip
#              "collapse turn": "R1"
#}
            collapse_turn:str = event["collapse turn"] # for example R1
            collapse_turn_number:int = superposition_moves[event["collapse turn"]] # for example 0
            previous_boards:list[Board] = flatten_nested_list(master_board.traverse(collapse_turn_number+1))
            resulting_column:int = event["Final position"]
            
            # we need to prune the tree; cut off a certain branch
            # we look for bad branches, aka branches with the wrong result
            for previous_board in previous_boards:
                # print("[DEBUG] collapse Analysing")
                # previous_board.draw()
                is_valid = False
                for cell in previous_board.board[resulting_column]:
                     if cell is not None:
                          if cell.move == collapse_turn:
                               is_valid = True
                # previous_board is a bad branch

                if not is_valid:
                    previous_board.parent.remove_child(previous_board)
            # we need to basically copy all of the last nodes ( or think of a better solution)
            all_boards = master_board.list_all_children_and_self([])
            nodes = [board for board in all_boards if board.layer == i]
            for board in nodes:
                child_board = board.make_child(1)
        
        else:
            raise KeyError("RIP")
        all_boards:list[Board] = master_board.list_all_children_and_self([])
        for board in all_boards:
        #     print(type(board))
            if board.layer == i+1: # fkin off by 1 error /j
                print("----------------------------------------")
                board.draw()
                print("the layer of this board is: ", board.layer)
                print("Probability of this board is: ", board.get_total_probability())
            
        print("----------------------------------------")
        print("----------------------------------------")


m.mainloop()