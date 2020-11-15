from enum import Enum
import os
import itertools as it


# Env variables
INPUT_PATH = 'SamplePuzzle.txt'
WIN_CONFIG = ['12345670', '13572460']
OUTPUT_PATH = './output'
TIMEOUT = 60

# Cost of each type of move.
class COST(Enum):
    ZERO = 0
    REGULAR = 1
    WRAPPING = 2
    DIAGONAL = 3

# Possible type of move
class move_type(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    DIAG_DOWN_RIGHT = 5
    DIAG_DOWN_LEFT = 6
    DIAG_UP_RIGHT = 7
    DIAG_UP_LEFT = 8
    WRAP_UP = 9
    WRAP_DOWN = 10
    WRAP_RIGHT = 11
    WRAP_LEFT = 12

def get_sol_file(search_type, number):
    sol = open(os.path.join(OUTPUT_PATH, str(number) + search_type + 'solution.txt'), "w")
    return sol


def get_search_file(search_type, number):
    search = open(os.path.join(OUTPUT_PATH, str(number) + search_type + 'search.txt'), "w")
    return search

# Read the input file containing puzzles and process to a list of puzzles
def get_puzzles() -> list:
    file = open(INPUT_PATH, "r")
    puzzles = []
    for line in file:
        puzzles.append(line.rstrip('\n').replace(" ", ""))
    return puzzles

def move(puzzle, zero_idx, to_idx) -> str:
    if(zero_idx < to_idx):
        puzzle = puzzle[:zero_idx] + puzzle[to_idx] + puzzle[zero_idx+1:to_idx] + puzzle[zero_idx] + puzzle[to_idx+1:]
    else:
        puzzle = puzzle[:to_idx] + puzzle[zero_idx] + puzzle[to_idx+1:zero_idx] + puzzle[to_idx] + puzzle[zero_idx+1:]
    return puzzle

def get_moving_token(zero_idx: int, columns: int, rows: int, move: move_type) -> int:
    return {
        move_type.UP: zero_idx - columns,
        move_type.DOWN: zero_idx + columns,
        move_type.LEFT: zero_idx - 1,
        move_type.RIGHT: zero_idx + 1,
        move_type.DIAG_DOWN_RIGHT: zero_idx + (columns + 1),
        move_type.DIAG_DOWN_LEFT: zero_idx + (columns - 1),
        move_type.DIAG_UP_RIGHT: zero_idx - (columns - 1),
        move_type.DIAG_UP_LEFT: zero_idx - (columns + 1),
        move_type.WRAP_UP: zero_idx - columns * (rows - 1),
        move_type.WRAP_DOWN: zero_idx + columns * (rows - 1),
        move_type.WRAP_RIGHT: zero_idx + (columns - 1),
        move_type.WRAP_LEFT: zero_idx - (columns - 1)
    }[move]

class new_config:
    def __init__(self, puzzle, cost, predecessor, token_to_move, gValue = 0, hValue = 0, fValue = 0):
        self.puzzle, self.cost, self.predecessor, self.token_to_move = puzzle, cost, predecessor, token_to_move
        self.gValue, self.hValue, self.fValue = gValue, hValue, fValue

    # Calculate the heuristic h with the given function
    def calculateH(self, funcH):
        self.hValue = funcH(self.puzzle)

    def calculateG(self, cumulative_cost):
        gValue = self.cost + cumulative_cost

    def calculateF(self):
        self.fValue = self.gValue + self.hValue
        return self.fValue


def find_possible_paths(puzzle, opened= [], closed=[], columns= 4, rows= 2, cumulative_cost = None, funcH = None):
    # Check out all possible 1-step move from the given puzzle.
    # Return the new OPEN list based on the moves gathered.

    paths = []
    zero_idx = puzzle.index('0')
    last_idx = (columns * rows) - 1

    # DIRECTION MOVES
    for config in check_direction_moves(puzzle, columns, rows, zero_idx, last_idx): paths.append(config)

    # DIAG MOVES
    for config in check_diag_moves(puzzle, columns, rows, zero_idx, last_idx): paths.append(config)

    # CORNER MOVES
    for config in check_corner_moves(puzzle, columns, rows, zero_idx, last_idx): paths.append(config)

    # Calculate g (if presents)
    if(cumulative_cost != None):
        for config in paths:
            config.calculateG(cumulative_cost)

    # Calculate h (if presents)
    if(funcH != None):
        for config in paths:
            config.calculateH(funcH)

    # Exclude paths in closed list (if provided)
    if closed != []:
        closed_paths = [x.puzzle for x in closed]
        paths = set(paths)
        paths = [config for config in paths if config.puzzle not in closed_paths]

    # No duplicate paths in open list: replace existing with lowest cost path or add new path
    for path in paths:
        open_idx = get_tuple_index(opened, path.puzzle)
        if(open_idx and opened[open_idx].cost.value > path.cost.value):
            opened[open_idx] = path
        elif(not open_idx):
            opened.append(path)

    return opened

def get_tuple_index(l, value):
    for pos,t in enumerate(l):
        if t.puzzle == value:
            return pos
    return None

def check_direction_moves(puzzle, columns, rows, zero_idx, last_idx):
    paths = []

     # Check move UP - regular cost
    temp_moving_token = get_moving_token(zero_idx, columns, rows, move_type.UP)
    if(temp_moving_token >= 0):
        newPuzzle = move(puzzle, zero_idx, temp_moving_token)
        paths.append(new_config(newPuzzle, COST.REGULAR, puzzle, puzzle[temp_moving_token]))

    # Check move DOWN - regular cost
    temp_moving_token = get_moving_token(zero_idx, columns, rows, move_type.DOWN)
    if(temp_moving_token <= last_idx):
        newPuzzle = move(puzzle, zero_idx, temp_moving_token)
        paths.append(new_config(newPuzzle, COST.REGULAR, puzzle, puzzle[temp_moving_token]))

    # Check move RIGHT - regular cost
    temp_moving_token = get_moving_token(zero_idx, columns, rows, move_type.RIGHT)
    if(temp_moving_token <= last_idx):
        # moving right is illegal is on rightmost positions of the board
        if((zero_idx + 1) % columns != 0):
            newPuzzle = move(puzzle, zero_idx, temp_moving_token)
            paths.append(new_config(newPuzzle, COST.REGULAR, puzzle, puzzle[temp_moving_token]))

    # Check move LEFT - regular cost
    temp_moving_token = get_moving_token(zero_idx, columns, rows, move_type.LEFT)
    if(temp_moving_token >= 0):
        # moving left is illegal is on leftmost positions of the board
        if(zero_idx % columns != 0):
            newPuzzle = move(puzzle, zero_idx, temp_moving_token)
            paths.append(new_config(newPuzzle, COST.REGULAR, puzzle, puzzle[temp_moving_token]))

    return paths

def check_diag_moves(puzzle, columns, rows, zero_idx, last_idx):
    paths = []

     # Check move DIAG DOWN RIGHT - diagonal cost
    temp_moving_token = get_moving_token(zero_idx, columns, rows, move_type.DIAG_DOWN_RIGHT)
    if(temp_moving_token <= last_idx):
        # moving down right is illegal is on rightmost positions of the board
        if((zero_idx + 1) % columns != 0):
            newPuzzle = move(puzzle, zero_idx, temp_moving_token)
            paths.append(new_config(newPuzzle, COST.DIAGONAL, puzzle, puzzle[temp_moving_token]))

    # Check move DIAG DOWN LEFT - diagonal/wrapping cost
    temp_moving_token = get_moving_token(zero_idx, columns, rows, move_type.DIAG_DOWN_LEFT)
    if(temp_moving_token <= last_idx):
        # moving down left is illegal is on leftmost positions of the board
        if(zero_idx % columns != 0):
            newPuzzle = move(puzzle, zero_idx, temp_moving_token)
            paths.append(new_config(newPuzzle, COST.DIAGONAL, puzzle, puzzle[temp_moving_token]))

    # Check move DIAG UP RIGHT - wrapping/diagonal cost
    temp_moving_token = get_moving_token(zero_idx, columns, rows, move_type.DIAG_UP_RIGHT)
    if(temp_moving_token >= 0):
        # moving up right is illegal is on rightmost positions of the board
        if((zero_idx + 1) % columns != 0):
            newPuzzle = move(puzzle, zero_idx, temp_moving_token)
            paths.append(new_config(newPuzzle, COST.DIAGONAL, puzzle, puzzle[temp_moving_token]))

    # Check move DIAG UP LEFT - diagonal cost
    temp_moving_token = get_moving_token(zero_idx, columns, rows, move_type.DIAG_UP_LEFT)
    if(temp_moving_token >= 0):
        # moving up left is illegal is on left-most positions of the board
        if(zero_idx % columns != 0):
            newPuzzle = move(puzzle, zero_idx, temp_moving_token)
            paths.append(new_config(newPuzzle, COST.DIAGONAL, puzzle, puzzle[temp_moving_token]))

    return paths


def check_corner_moves(puzzle, columns, rows, zero_idx, last_idx):
    paths = []

    # Check moves if zero_idx is on upper left corner position
    if(zero_idx == 0):
        # DIAGONAL
        temp_moving_token = last_idx
        newPuzzle = move(puzzle, zero_idx, temp_moving_token)
        paths.append(new_config(newPuzzle, COST.DIAGONAL, puzzle, puzzle[temp_moving_token]))

        # WRAP RIGHT
        temp_moving_token = get_moving_token(zero_idx, columns, rows, move_type.WRAP_RIGHT)
        newPuzzle = move(puzzle, zero_idx, temp_moving_token)
        paths.append(new_config(newPuzzle, COST.WRAPPING, puzzle, puzzle[temp_moving_token]))

        # WRAP DOWN
        if(rows > 2):
            temp_moving_token = get_moving_token(zero_idx, columns, rows, move_type.WRAP_DOWN)
            newPuzzle = move(puzzle, zero_idx, temp_moving_token)
            paths.append(new_config(newPuzzle, COST.WRAPPING, puzzle, puzzle[temp_moving_token]))

    # Check moves if zero_idx is on upper right corner position
    elif(zero_idx == columns - 1):
        # DIAGONAL
        temp_moving_token = last_idx - columns + 1
        newPuzzle = move(puzzle, zero_idx, temp_moving_token)
        paths.append(new_config(newPuzzle, COST.DIAGONAL, puzzle, puzzle[temp_moving_token]))

        # WRAP LEFT
        temp_moving_token = get_moving_token(zero_idx, columns, rows, move_type.WRAP_LEFT)
        newPuzzle = move(puzzle, zero_idx, temp_moving_token)
        paths.append(new_config(newPuzzle, COST.WRAPPING, puzzle, puzzle[temp_moving_token]))

        # WRAP DOWN
        if(rows > 2):
            temp_moving_token = get_moving_token(zero_idx, columns, rows, move_type.WRAP_DOWN)
            newPuzzle = move(puzzle, zero_idx, temp_moving_token)
            paths.append(new_config(newPuzzle, COST.WRAPPING, puzzle, puzzle[temp_moving_token]))

    # Check moves if zero_idx is on lower left corner position
    elif(zero_idx == last_idx - columns + 1):
        # DIAGONAL
        temp_moving_token = columns - 1
        newPuzzle = move(puzzle, zero_idx, temp_moving_token)
        paths.append(new_config(newPuzzle, COST.DIAGONAL, puzzle, puzzle[temp_moving_token]))

        # WRAP RIGHT
        temp_moving_token = get_moving_token(zero_idx, columns, rows, move_type.WRAP_RIGHT)
        newPuzzle = move(puzzle, zero_idx, temp_moving_token)
        paths.append(new_config(newPuzzle, COST.WRAPPING, puzzle, puzzle[temp_moving_token]))

        # WRAP UP
        if(rows > 2):
            temp_moving_token = get_moving_token(zero_idx, columns, rows, move_type.WRAP_UP)
            newPuzzle = move(puzzle, zero_idx, temp_moving_token)
            paths.append(new_config(newPuzzle, COST.WRAPPING, puzzle, puzzle[temp_moving_token]))

    # Check moves if zero_idx is on lower right corner position
    elif(zero_idx == last_idx):
        # DIAGONAL
        temp_moving_token = 0
        newPuzzle = move(puzzle, zero_idx, temp_moving_token)
        paths.append(new_config(newPuzzle, COST.DIAGONAL, puzzle, puzzle[temp_moving_token]))

        # WRAP LEFT
        temp_moving_token = get_moving_token(zero_idx, columns, rows, move_type.WRAP_LEFT)
        newPuzzle = move(puzzle, zero_idx, temp_moving_token)
        paths.append(new_config(newPuzzle, COST.WRAPPING, puzzle, puzzle[temp_moving_token]))

        # WRAP UP
        if(rows > 2):
            temp_moving_token = get_moving_token(zero_idx, columns, rows, move_type.WRAP_UP)
            newPuzzle = move(puzzle, zero_idx, temp_moving_token)
            paths.append(new_config(newPuzzle, COST.WRAPPING, puzzle, puzzle[temp_moving_token]))

    return paths
