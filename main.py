ClearRow = ["X", "X", "X", "X", "X", "X"]
SYMBOLS = ["A","B","C","D"]
from copy import deepcopy
class Puzzle:


    def __init__(
            self,
            positions: list[tuple[int, int]],
            switches: list[bool] = None,
            last_move_was_rows:bool = None,
            )-> None:
        if switches is None:
            switches = [True, True, True, True]
        self.switches = switches
        self.positions = positions
        self.last_move_was_rows = last_move_was_rows
        # self.A = positions[0]
        # self.B = positions[1]
        # self.C = positions[2]
        # self.D = positions[3]

        # Make Canvas
        self.matrix = [ClearRow[:], ClearRow[:], ClearRow[:], ClearRow[:], ClearRow[:], ClearRow[:]]
        # fill center square
        for row in range(6):
            for column in range(6):
                if (0 < row < 5) and (0 < column < 5):
                    self.matrix[row][column] = " "

        # add switch places
        self.set_switches(switches)

        # set positions
        for i, symbol in enumerate(SYMBOLS):
            position = positions[i]
            self.matrix[position[0]][position[1]] = symbol

    def set_switches(self, switches):
        base_coordinates_rows = [(1, 0), (2, 5)]
        base_coordinates_columns = [(0, 1), (5, 2)]
        stumps = []
        # switch 1
        if switches[0]:
            offsets = [(2, 0), (2, 0)]
        else: 
            offsets = [(3, 0), (1, 0)]
        stumps.append([base_coordinates_rows[0][i] + offsets[0][i] for i in [0,1]])
        stumps.append([base_coordinates_rows[1][i] + offsets[1][i] for i in [0,1]])
        # switch 2
        if switches[1]:
            offsets = [(0, 0), (0, 0)]
        else: 
            offsets = [(1, 0), (-1, 0)]
        stumps.append([base_coordinates_rows[0][i] + offsets[0][i] for i in [0,1]])
        stumps.append([base_coordinates_rows[1][i] + offsets[1][i] for i in [0,1]])
        for stump in stumps:
            self.matrix[stump[0]][ stump[1]]=" "
        # switch 3
        if switches[2]:
            offsets = [(0, 0), (0, 0)]
        else: 
            offsets = [(0, 1), (0, -1)]
        stumps.append([base_coordinates_columns[0][i] + offsets[0][i] for i in [0,1]])
        stumps.append([base_coordinates_columns[1][i] + offsets[1][i] for i in [0,1]])
        for stump in stumps: 
            self.matrix[stump[0]][ stump[1]]=" "
        # switch 3
        if switches[3]:
            offsets = [(0, 2), (0, 2)]
        else: 
            offsets = [(0, 3), (0, 1)]
        stumps.append([base_coordinates_columns[0][i] + offsets[0][i] for i in [0,1]])
        stumps.append([base_coordinates_columns[1][i] + offsets[1][i] for i in [0,1]])
        for stump in stumps: 
            self.matrix[stump[0]][ stump[1]]=" "


    def __repr__(self) -> str:
        stringmatrix = [str(row) for row in self.matrix]
        return "\n".join(stringmatrix)
    

    def switch(self, label:int) -> None:
        if label > 1:
            self.switch_column(label)
            self.last_move_was_rows = False
        else:
            self.switch_row(label)
            self.last_move_was_rows = True
        self.switches[label] = not self.switches[label]
    
    def switch_row(self, label):
        if label == 0:
            offset = 3
        else:
            offset = 1
        if self.switches[label]:
            self.shift_right(row=offset)
            self.shift_left(row=offset+1)
        else:
            self.shift_right(row=offset+1)
            self.shift_left(row=offset)

    def shift_right(self, row):
        for index in range(5):
            self.matrix[row][5 - index] = self.matrix[row][5 - index - 1]
        self.matrix[row][0] = "X"

    def shift_left(self, row):
        for index in range(5):
            self.matrix[row][index] = self.matrix[row][index + 1]
        self.matrix[row][5] = "X"

    def switch_column(self, label):
        if label == 2:
            offset = 1
        else:
            offset = 3
        if not self.switches[label]:
            self.shift_down(column=offset)
            self.shift_up(column=offset+1)
        else:
            self.shift_down(column=offset+1)
            self.shift_up(column=offset)

    def shift_up(self, column):
        for index in range(5):
            self.matrix[5 - index][column] = self.matrix[5 - index - 1][column]
        self.matrix[0][column] = "X"

    def shift_down(self, column):
        for index in range(5):
            self.matrix[index][column] = self.matrix[index + 1][column]
        self.matrix[5][column] = "X"
    
    def is_solved(self)->bool:
        center_positions = [(2, 2), (2, 3), (3, 2), (3, 3)]
        truth_vector = [self.matrix[position[0]][position[1]] == SYMBOLS[index] 
                        for index, position in enumerate(center_positions)]
        return all(truth_vector)
    
    def solve(self):
        # set depth
        depth = 4
        self.done = self.is_solved()
        self.path = []
        self.final_path = None
        # pick direction: columns
        self.last_move_was_rows = True
        # in that direction, throw switches A, B, A, B
        self.continute_solve(depth)

        # pick direction: rows
        self.last_move_was_rows = False
        # in that direction, throw switches A, B, A, B
        self.continute_solve(depth)

        if not self.done:
            print(f"NO SOLUTION REACHED WITHIN {depth} MOVES")
        else:
            print(f"SOLUTION REACHED WITHIN {depth} MOVES!:\n")
            print(self.final_path)

    
    def continute_solve(self, depth):
        my_copy = deepcopy(self.matrix[:])
        my_path = deepcopy(self.path)
        my_switches = deepcopy(self.switches)
        if not self.done:
            if depth == 0:
                return
            if self.last_move_was_rows:
                self.move(depth, 2)
                self.move(depth, 3)
                self.move(depth, 2)
                # self.move(depth, path, 3, done)
            else:
                self.move(depth, 0)
                self.move(depth, 1)
                self.move(depth, 0)
                # self.move(depth, path, 1, done)
            self.matrix = my_copy
            self.path = my_path
            self.switches = my_switches


    def move(self, depth, direction):
        self.switch(direction)
        self.path.append(direction)
        if self.is_solved():
            self.done = True
            self.final_path = self.path[:]
        self.continute_solve(depth-1)



solved = Puzzle(positions=[(2, 2), (2, 3), (3, 2), (3, 3)])
star_puzzle = Puzzle(positions=[(0, 3), (4, 5), (1, 0), (5, 2)])
# _puzzle = Puzzle(positions=[(, ), (, ), (, ), (, )])
almost_puzzle = Puzzle(positions=[(2, 2), (2, 3), (3, 2), (2, 5)])
curtains_puzzle = Puzzle(positions=[(3, 0), (4, 5), (2, 3), (2, 2)])
boat_puzzle = Puzzle(positions=[(2, 2), (1, 3), (2, 3), (3, 3)])
fakeout_puzzle = Puzzle(positions=[(3, 0), (0, 1), (4, 2), (2, 5)])
slide_puzzle = Puzzle(positions=[(3, 0), (2, 3), (4, 2), (2, 1)])
slice_puzzle = Puzzle(positions=[(3, 4), (3, 1), (3, 2), (3, 3)])
puzzle = star_puzzle
print(puzzle)
puzzle.solve()

# simple
# [0, 1, 2, 3, 0, 1, 2, 3] # star
# easy
# [0, 3, 1, 3, 0, 3, 1, 3] # almost
# [3, 1, 2, 1, 3, 1, 2, 1] # Boat 
# medium
# [2, 3, 0, 1, 2, 0, 1, 3] # slide
# [2, 0, 3, 1, 2, 3, 0, 1] # fakeout
# hard
# [2, 3, 1, 2, 3, 0, 2, 0, 1, 2] # slice
# [3, 1, 2, 3, 0, 2, 3, 0, 1, 3] # curtains