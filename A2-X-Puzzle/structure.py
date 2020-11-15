"""
File with data structures being used for all the searches
"""

from enum import Enum
import copy

WIN_CONFIG = [
    [1, 2, 3, 4, 5, 6, 7, 0],
    [1, 3, 5, 7, 2, 4, 6, 0]
]

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

class puzzle:
    def __init__(self, content, columns, rows):
        """
        content: a list of integer represents the configuration.
        columns, rows: the number of columns, rows in the puzzle.
        """
        self.content, self.columns, self.rows = content, columns, rows
        self.zero_idx = self.content.index(0)
        self.last_idx = (columns * rows) - 1

    # Make a move in a temp puzzle and return that puzzle
    def move(self, to_idx: int):
        temp = copy.deepcopy(self)
        temp.content[self.zero_idx], temp.content[to_idx] = temp.content[to_idx], temp.content[self.zero_idx]
        return temp

    def is_win(self):
        for config in WIN_CONFIG:
            if(config == self.content):
                return True
        return False

    def is_equal(self, other):
        return self.content == other.content

    def to_string(self):
        output = ''
        for char in self.content:
            output += str(char) + ' '
        return output

class new_config:
    def __init__(self, puzzle: puzzle, cost, predecessor: puzzle, token_to_move, gValue = 0, hValue = 0, fValue = 0):
        self.puzzle, self.cost, self.predecessor, self.token_to_move = puzzle, cost, predecessor, token_to_move
        self.gValue, self.hValue, self.fValue = gValue, hValue, fValue

    # Calculate the heuristic h with the given function
    def calculateH(self, funcH):
        self.hValue = funcH(self.puzzle)

    def calculateG(self, cumulative_cost):
        self.gValue = self.cost.value + cumulative_cost

    def calculateF(self):
        self.fValue = self.gValue + self.hValue
        return self.fValue

    def to_file(self, writeF = False, writeG = False, writeH =False):
        output = ''
        output += (str(self.fValue) + ' ') if writeF else (str(0) + ' ')
        output += (str(self.gValue) + ' ') if writeG else (str(0) + ' ')
        output += (str(self.hValue) + ' ') if writeH else (str(0) + ' ')
        output += self.puzzle.to_string() + ' '
        return output