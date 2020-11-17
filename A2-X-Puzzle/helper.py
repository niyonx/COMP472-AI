"""
File containing helper functions for searching algorithm
"""

import os
import itertools as it
from structure import *

# Env variables
INPUT_PATH = 'SamplePuzzle.txt'
OUTPUT_PATH = './output'
TIMEOUT = 60

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
        puzzles.append(line.rstrip('\n'))
    return puzzles

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


def find_possible_paths(curr_puzzle: puzzle, opened, closed=[], cumulative_cost = None, funcH = None):
    # Check out all possible 1-step move from the given puzzle.
    # Return the new OPEN list based on the moves gathered.

    paths = []
    zero_idx = curr_puzzle.zero_idx
    last_idx = curr_puzzle.last_idx
    columns = curr_puzzle.columns
    rows = curr_puzzle.rows

    # DIRECTION MOVES
    for config in check_direction_moves(curr_puzzle, columns, rows, zero_idx, last_idx): paths.append(config)

    # DIAG MOVES
    for config in check_diag_moves(curr_puzzle, columns, rows, zero_idx, last_idx): paths.append(config)

    # CORNER MOVES
    for config in check_corner_moves(curr_puzzle, columns, rows, zero_idx, last_idx): paths.append(config)

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
        closed_paths = [x.puzzle.to_string() for x in closed]
        paths = set(paths)
        paths = [config for config in paths if config.puzzle.to_string() not in closed_paths]

    # No duplicate paths in open list: replace existing with lowest cost path or add new path
    for path in paths:
        open_idx = get_tuple_index(opened, path)
        if(open_idx and opened[open_idx].cost.value > path.cost.value):
            opened[open_idx] = path
        elif(open_idx == None):
            opened.append(path)

    return opened

def get_tuple_index(l, target):
    for pos in range(len(l)):
        if(l[pos].puzzle.is_equal(target.puzzle)):
            return pos
    return None

def check_direction_moves(curr_puzzle: puzzle, columns, rows, zero_idx, last_idx):
    paths = []

    # Check move UP - regular cost
    temp_moving_idx = get_moving_token(zero_idx, columns, rows, move_type.UP)
    if(temp_moving_idx >= 0):
        newPuzzle = curr_puzzle.move(temp_moving_idx)
        paths.append(new_config(newPuzzle, COST.REGULAR, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

    # Check move DOWN - regular cost
    temp_moving_idx = get_moving_token(zero_idx, columns, rows, move_type.DOWN)
    if(temp_moving_idx <= last_idx):
        newPuzzle = curr_puzzle.move(temp_moving_idx)
        paths.append(new_config(newPuzzle, COST.REGULAR, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

    # Check move RIGHT - regular cost
    temp_moving_idx = get_moving_token(zero_idx, columns, rows, move_type.RIGHT)
    if(temp_moving_idx <= last_idx):
        # moving right is illegal is on rightmost positions of the board
        if((zero_idx + 1) % columns != 0):
            newPuzzle = curr_puzzle.move(temp_moving_idx)
            paths.append(new_config(newPuzzle, COST.REGULAR, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

    # Check move LEFT - regular cost
    temp_moving_idx = get_moving_token(zero_idx, columns, rows, move_type.LEFT)
    if(temp_moving_idx >= 0):
        # moving left is illegal is on leftmost positions of the board
        if(zero_idx % columns != 0):
            newPuzzle = curr_puzzle.move(temp_moving_idx)
            paths.append(new_config(newPuzzle, COST.REGULAR, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

    return paths

def check_diag_moves(curr_puzzle, columns, rows, zero_idx, last_idx):
    paths = []

    # Check move DIAG DOWN RIGHT - diagonal cost
    temp_moving_idx = get_moving_token(zero_idx, columns, rows, move_type.DIAG_DOWN_RIGHT)
    if(temp_moving_idx <= last_idx):
        # moving down right is illegal is on rightmost positions of the board
        if((zero_idx + 1) % columns != 0):
            newPuzzle = curr_puzzle.move(temp_moving_idx)
            paths.append(new_config(newPuzzle, COST.DIAGONAL, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

    # Check move DIAG DOWN LEFT - diagonal/wrapping cost
    temp_moving_idx = get_moving_token(zero_idx, columns, rows, move_type.DIAG_DOWN_LEFT)
    if(temp_moving_idx <= last_idx):
        # moving down left is illegal is on leftmost positions of the board
        if(zero_idx % columns != 0):
            newPuzzle = curr_puzzle.move(temp_moving_idx)
            paths.append(new_config(newPuzzle, COST.DIAGONAL, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

    # Check move DIAG UP RIGHT - wrapping/diagonal cost
    temp_moving_idx = get_moving_token(zero_idx, columns, rows, move_type.DIAG_UP_RIGHT)
    if(temp_moving_idx >= 0):
        # moving up right is illegal is on rightmost positions of the board
        if((zero_idx + 1) % columns != 0):
            newPuzzle = curr_puzzle.move(temp_moving_idx)
            paths.append(new_config(newPuzzle, COST.DIAGONAL, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

    # Check move DIAG UP LEFT - diagonal cost
    temp_moving_idx = get_moving_token(zero_idx, columns, rows, move_type.DIAG_UP_LEFT)
    if(temp_moving_idx >= 0):
        # moving up left is illegal is on left-most positions of the board
        if(zero_idx % columns != 0):
            newPuzzle = curr_puzzle.move(temp_moving_idx)
            paths.append(new_config(newPuzzle, COST.DIAGONAL, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

    return paths


def check_corner_moves(curr_puzzle, columns, rows, zero_idx, last_idx):
    paths = []

    # Check moves if zero_idx is on upper left corner position
    if(zero_idx == 0):
        # DIAGONAL
        temp_moving_idx = last_idx
        newPuzzle = curr_puzzle.move(temp_moving_idx)
        paths.append(new_config(newPuzzle, COST.DIAGONAL, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

        # WRAP RIGHT
        temp_moving_idx = get_moving_token(zero_idx, columns, rows, move_type.WRAP_RIGHT)
        newPuzzle = curr_puzzle.move(temp_moving_idx)
        paths.append(new_config(newPuzzle, COST.WRAPPING, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

        # WRAP DOWN
        if(rows > 2):
            temp_moving_idx = get_moving_token(zero_idx, columns, rows, move_type.WRAP_DOWN)
            newPuzzle =curr_puzzle.move(temp_moving_idx)
            paths.append(new_config(newPuzzle, COST.WRAPPING, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

    # Check moves if zero_idx is on upper right corner position
    elif(zero_idx == columns - 1):
        # DIAGONAL
        temp_moving_idx = last_idx - columns + 1
        newPuzzle = curr_puzzle.move(temp_moving_idx)
        paths.append(new_config(newPuzzle, COST.DIAGONAL, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

        # WRAP LEFT
        temp_moving_idx = get_moving_token(zero_idx, columns, rows, move_type.WRAP_LEFT)
        newPuzzle = curr_puzzle.move(temp_moving_idx)
        paths.append(new_config(newPuzzle, COST.WRAPPING, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

        # WRAP DOWN
        if(rows > 2):
            temp_moving_idx = get_moving_token(zero_idx, columns, rows, move_type.WRAP_DOWN)
            newPuzzle = curr_puzzle.move(temp_moving_idx)
            paths.append(new_config(newPuzzle, COST.WRAPPING, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

    # Check moves if zero_idx is on lower left corner position
    elif(zero_idx == last_idx - columns + 1):
        # DIAGONAL
        temp_moving_idx = columns - 1
        newPuzzle = curr_puzzle.move(temp_moving_idx)
        paths.append(new_config(newPuzzle, COST.DIAGONAL, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

        # WRAP RIGHT
        temp_moving_idx = get_moving_token(zero_idx, columns, rows, move_type.WRAP_RIGHT)
        newPuzzle = curr_puzzle.move(temp_moving_idx)
        paths.append(new_config(newPuzzle, COST.WRAPPING, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

        # WRAP UP
        if(rows > 2):
            temp_moving_idx = get_moving_token(zero_idx, columns, rows, move_type.WRAP_UP)
            newPuzzle = curr_puzzle.move(temp_moving_idx)
            paths.append(new_config(newPuzzle, COST.WRAPPING, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

    # Check moves if zero_idx is on lower right corner position
    elif(zero_idx == last_idx):
        # DIAGONAL
        temp_moving_idx = 0
        newPuzzle = curr_puzzle.move(temp_moving_idx)
        paths.append(new_config(newPuzzle, COST.DIAGONAL, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

        # WRAP LEFT
        temp_moving_idx = get_moving_token(zero_idx, columns, rows, move_type.WRAP_LEFT)
        newPuzzle = curr_puzzle.move(temp_moving_idx)
        paths.append(new_config(newPuzzle, COST.WRAPPING, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

        # WRAP UP
        if(rows > 2):
            temp_moving_idx = get_moving_token(zero_idx, columns, rows, move_type.WRAP_UP)
            newPuzzle = curr_puzzle.move(temp_moving_idx)
            paths.append(new_config(newPuzzle, COST.WRAPPING, curr_puzzle, curr_puzzle.content[temp_moving_idx]))

    return paths