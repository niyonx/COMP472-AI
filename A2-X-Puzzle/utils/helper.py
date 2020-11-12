from enum import Enum
import os

# Env variables
INPUT_PATH = 'SamplePuzzle.txt'
WIN_CONFIG = ['12345670', '13572460']
OUTPUT_PATH = './output'
TIMEOUT = 60

# Cost of each type of move.
class COST(Enum):
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

def find_possible_paths(puzzle, closed=[], columns= 4, rows= 2):
    # returns list of all possible 1-step paths in form (path, cost, predecessor, token_to_move) for any board configurations

    paths = []
    zero_idx = puzzle.index('0')
    last_idx = (columns * rows) - 1
    
    # DIRECTION MOVES

    # Check move UP - regular cost
    if(get_moving_token(zero_idx, columns, rows, move_type.UP) >= 0):
        movingToken = get_moving_token(zero_idx, columns, rows, move_type.UP)
        paths.append((move(puzzle, zero_idx, movingToken), COST.REGULAR, puzzle, movingToken))

    # Check move DOWN - regular cost
    if(get_moving_token(zero_idx, columns, rows, move_type.DOWN) <= last_idx):
        movingToken = get_moving_token(zero_idx, columns, rows, move_type.DOWN)
        paths.append((move(puzzle, zero_idx, movingToken), COST.REGULAR, puzzle, movingToken))

    # Check move RIGHT - regular cost
    if(get_moving_token(zero_idx, columns, rows, move_type.RIGHT) <= last_idx):
        # moving right is illegal is on rightmost positions of the board 
        if((zero_idx + 1) % columns != 0):
            movingToken = get_moving_token(zero_idx, columns, rows, move_type.RIGHT)
            paths.append((move(puzzle, zero_idx, movingToken), COST.REGULAR, puzzle, movingToken))

    # Check move LEFT - regular cost
    if(get_moving_token(zero_idx, columns, rows, move_type.LEFT) >= 0):
        # moving left is illegal is on leftmost positions of the board 
        if(zero_idx % columns != 0): 
            movingToken = get_moving_token(zero_idx, columns, rows, move_type.LEFT)
            paths.append((move(puzzle, zero_idx, movingToken), COST.REGULAR, puzzle, movingToken))

    # DIAG MOVES

    # Check move DIAG DOWN RIGHT - diagonal cost
    if(get_moving_token(zero_idx, columns, rows, move_type.DIAG_DOWN_RIGHT) <= last_idx):
        # moving down right is illegal is on rightmost positions of the board 
        if((zero_idx + 1) % columns != 0): 
            movingToken = get_moving_token(zero_idx, columns, rows, move_type.DIAG_DOWN_RIGHT)
            paths.append((move(puzzle, zero_idx, movingToken), COST.DIAGONAL, puzzle, movingToken))

    # Check move DIAG DOWN LEFT - diagonal/wrapping cost
    if(get_moving_token(zero_idx, columns, rows, move_type.DIAG_DOWN_LEFT) <= last_idx):
        # moving down left is illegal is on leftmost positions of the board 
        if(zero_idx % columns != 0): 
            movingToken = get_moving_token(zero_idx, columns, rows, move_type.DIAG_DOWN_LEFT)
            paths.append((move(puzzle, zero_idx, movingToken), COST.DIAGONAL, puzzle, movingToken))
    
    # Check move DIAG UP RIGHT - wrapping/diagonal cost
    if(get_moving_token(zero_idx, columns, rows, move_type.DIAG_UP_RIGHT) >= 0):
        # moving up right is illegal is on rightmost positions of the board 
        if((zero_idx + 1) % columns != 0): 
            movingToken = get_moving_token(zero_idx, columns, rows, move_type.DIAG_UP_RIGHT)
            paths.append((move(puzzle, zero_idx, movingToken), COST.DIAGONAL, puzzle, movingToken))

    # Check move DIAG UP LEFT - diagonal cost
    if(get_moving_token(zero_idx, columns, rows, move_type.DIAG_UP_LEFT) >= 0):
        # moving up left is illegal is on left-most positions of the board 
        if(zero_idx % columns != 0): 
            movingToken = get_moving_token(zero_idx, columns, rows, move_type.DIAG_UP_LEFT)
            paths.append((move(puzzle, zero_idx, movingToken), COST.DIAGONAL, puzzle, movingToken))

    # CORNER MOVES

    # Check moves if zero_idx is on upper left corner position
    if(zero_idx == 0):
        # DIAGONAL
        movingToken = last_idx
        paths.append((move(puzzle, zero_idx, movingToken), COST.DIAGONAL, puzzle, movingToken))
        # # WRAP RIGHT
        movingToken = get_moving_token(zero_idx, columns, rows, move_type.WRAP_RIGHT)
        paths.append((move(puzzle, zero_idx, movingToken), COST.WRAPPING, puzzle, movingToken))
        # WRAP DOWN
        if(rows > 2):
            movingToken = get_moving_token(zero_idx, columns, rows, move_type.WRAP_DOWN)
            paths.append((move(puzzle, zero_idx, movingToken), COST.WRAPPING, puzzle, movingToken))

    # Check moves if zero_idx is on upper right corner position
    elif(zero_idx == columns - 1):
        # DIAGONAL
        movingToken = last_idx - columns + 1
        paths.append((move(puzzle, zero_idx, movingToken), COST.DIAGONAL, puzzle, movingToken))
        # WRAP LEFT
        movingToken = get_moving_token(zero_idx, columns, rows, move_type.WRAP_LEFT)
        paths.append((move(puzzle, zero_idx, movingToken), COST.WRAPPING, puzzle, movingToken))
        # WRAP DOWN
        if(rows > 2):
            movingToken = get_moving_token(zero_idx, columns, rows, move_type.WRAP_DOWN)
            paths.append((move(puzzle, zero_idx, movingToken), COST.WRAPPING, puzzle, movingToken))

    # # Check moves if zero_idx is on lower left corner position
    elif(zero_idx == last_idx - columns + 1):
        # DIAGONAL
        movingToken = columns - 1
        paths.append((move(puzzle, zero_idx, movingToken), COST.DIAGONAL, puzzle, movingToken))
        # WRAP RIGHT
        movingToken = get_moving_token(zero_idx, columns, rows, move_type.WRAP_RIGHT)
        paths.append((move(puzzle, zero_idx, movingToken), COST.WRAPPING, puzzle, movingToken))
        # WRAP UP
        if(rows > 2):
            movingToken = get_moving_token(zero_idx, columns, rows, move_type.WRAP_UP)
            paths.append((move(puzzle, zero_idx, movingToken), COST.WRAPPING, puzzle, movingToken))

    # Check moves if zero_idx is on lower right corner position
    elif(zero_idx == last_idx):
        # DIAGONAL
        movingToken = 0
        paths.append((move(puzzle, zero_idx, movingToken), COST.DIAGONAL, puzzle, movingToken))
        # WRAP LEFT
        movingToken = get_moving_token(zero_idx, columns, rows, move_type.WRAP_LEFT)
        paths.append((move(puzzle, zero_idx, movingToken), COST.WRAPPING, puzzle, movingToken))
        # WRAP UP
        if(rows > 2):
            movingToken = get_moving_token(zero_idx, columns, rows, move_type.WRAP_UP)
            paths.append((move(puzzle, zero_idx, movingToken), COST.WRAPPING, puzzle, movingToken))


    # Exclude closed paths (if provided)
    if closed != []:
        paths = set(paths)
        paths = [x for x in paths if x[0] not in closed[0]]

    return paths


# EXAMPLES 

# print(move('30142657',1,0)) # '03142657'

# print(find_possible_paths('30142657', [('32140617', 1)])) # [('32140657', 3, '30142657'), ('35142607', 3, '30142657'), ('36142057', 1, '30142657'), ('03142657', 1, '30142657'), ('31042657', 1, '30142657')]

# print(find_possible_paths('30142657')) # [('36142057', 1, '30142657'), ('03142657', 1, '30142657'), ('31042657', 1, '30142657'), ('35142607', 3, '30142657'), ('32140657', 3, '30142657')]