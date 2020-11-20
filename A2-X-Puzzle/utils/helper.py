"""
File containing helper functions for searching algorithm
"""

import os
import itertools as it
from utils.structure import *
from utils.HeuristicFunc import *

# Env variables
INPUT_PATH = 'SamplePuzzle.txt'
OUTPUT_PATH = './output'
TIMEOUT = 60

def get_sol_file(search_type, number):
    return open(os.path.join(OUTPUT_PATH, str(number) + search_type + 'solution.txt'), "w")


def get_search_file(search_type, number):
    return open(os.path.join(OUTPUT_PATH, str(number) + search_type + 'search.txt'), "w")

def print_analysis(sol_length, no_puzzles, search_length, no_sol, cost, time):
    print('Summary')
    print(f'\tSolution path total length: {sol_length}')
    if(no_puzzles - no_sol != 0):
        print(f'\tSolution path average length: {(sol_length/ (no_puzzles-no_sol)):.2f}')
    print(f'\tSearch path total length: {search_length}')
    print(f'\tSearch path average length: {(search_length/ no_puzzles):.2f}')
    print(f'\tTotal no of no solution: {no_sol}')
    print(f'\tAverage no of no solution: {(no_sol/ no_puzzles):.2f}')
    print(f'\tTotal cost: {cost}')
    if(no_puzzles - no_sol != 0):
        print(f'\tAverage cost: {(cost/ (no_puzzles-no_sol)):.2f}')
    print(f'\tTotal execution time: {time}')
    print(f'\tAverage execution time: {(time/no_puzzles):.2f}')

def get_funcH(number):
    if(number == 0):
        return h0
    if(number == 1):
        return h1
    return h2

# Read the input file containing puzzles and process to a list of puzzles
def get_puzzles(path) -> list:
    file = open(path, "r")
    return [line.rstrip('\n') for line in file]

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
    paths.extend([config for config in check_direction_moves(curr_puzzle, columns, rows, zero_idx, last_idx)])

    # DIAG MOVES
    paths.extend([config for config in check_diag_moves(curr_puzzle, columns, rows, zero_idx, last_idx)])

    # CORNER MOVES
    paths.extend([config for config in check_corner_moves(curr_puzzle, columns, rows, zero_idx, last_idx)])

    # Calculate g and f (if present)
    if(cumulative_cost != None and funcH): # A*
        for config in paths:
            config.calculateH(funcH)
            config.calculateG(cumulative_cost)
            config.calculateF()
        # Checking closed to place back in open if lower f value or ignore
        if closed != []:
            closed_paths = [x.puzzle.to_string() for x in closed]
            for i, closed_path in enumerate(closed_paths):
                for path in paths:
                    # Remove paths in closed which now has a lower f value in open
                    if(closed_path == path.puzzle.to_string() and closed[i].fValue > path.fValue):
                        del closed[i]
                        del closed_paths[i]
            # Include paths not in closed list (if provided)
            paths = [config for config in paths if config.puzzle.to_string() not in closed_paths]
    elif (funcH): # GBFS
        for config in paths:
            config.calculateH(funcH)
        # Include paths not in closed list (if provided)
        if closed != []:
            closed_paths = [x.puzzle.to_string() for x in closed]
            paths = [config for config in paths if config.puzzle.to_string() not in closed_paths]
    elif(cumulative_cost != None):
        for config in paths:
            config.calculateG(cumulative_cost)
        # Include paths not in closed list (if provided)
        if closed != []:
            closed_paths = [x.puzzle.to_string() for x in closed]
            paths = [config for config in paths if config.puzzle.to_string() not in closed_paths]

    # No duplicate paths in open list: replace existing with lowest cost path or add new path
    for path in paths:
        open_idx = get_tuple_index(opened, path)
        if(open_idx and opened[open_idx].cost.value > path.cost.value):
            opened[open_idx] = path
        elif(not open_idx):
            opened.append(path)

    return opened

def get_tuple_index(l, target):
    for pos in range(len(l)):
        if(l[pos].puzzle.is_equal(target.puzzle)):
            return pos
    return False

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
