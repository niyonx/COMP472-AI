def move(puzzle, zero_idx, to_idx):
    if(zero_idx < to_idx):
        puzzle = puzzle[:zero_idx] + puzzle[to_idx] + puzzle[zero_idx+1:to_idx] + puzzle[zero_idx] + puzzle[to_idx+1:]
    else:
        puzzle = puzzle[:to_idx] + puzzle[zero_idx] + puzzle[to_idx+1:zero_idx] + puzzle[to_idx] + puzzle[zero_idx+1:]
    return puzzle

def find_possible_paths(puzzle, closed=[]):
    # returns list of all possible paths in form (path, cost, predecessor)
    # TODO: when scaling, softcode values

    paths = []
    zero_idx = puzzle.index('0')
    column = 4

    # check move up
    if(zero_idx - 4 >= 0):
        paths.append((move(puzzle, zero_idx, zero_idx - 4),1, puzzle))
    # check move down
    if(zero_idx + 4 <= 7):
        paths.append((move(puzzle, zero_idx, zero_idx + 4),1, puzzle))
    # check move left
    if(zero_idx - 1 >= 0):
        paths.append((move(puzzle, zero_idx, zero_idx - 1),1, puzzle))
    # check move right
    if(zero_idx + 1 <= 7):
        paths.append((move(puzzle, zero_idx, zero_idx + 1),1, puzzle))
    # check move diag down-right
    if(zero_idx + 5 <= 7):
        paths.append((move(puzzle, zero_idx, zero_idx + 5),3, puzzle))
    # check move diag down-left
    if(zero_idx + 3 <= 7):
        # if zero_idx is in corner, diag move will lead to wrapping move e.g 01234567 to 31204567
        if(zero_idx % column == 0 or (zero_idx+1) % column == 0): # left corner or right corner
            paths.append((move(puzzle, zero_idx, zero_idx + 3),2, puzzle))
        else:
            paths.append((move(puzzle, zero_idx, zero_idx + 3),3, puzzle))
    # check move diag up-right
    if(zero_idx - 3 >= 0):
        if(zero_idx % column == 0 or (zero_idx+1) % column == 0): # left corner or right corner
            paths.append((move(puzzle, zero_idx, zero_idx - 3),2, puzzle))
        else:
            paths.append((move(puzzle, zero_idx, zero_idx - 3),3, puzzle))
    # check move diag up-left
    if(zero_idx - 5 >= 0):
        paths.append((move(puzzle, zero_idx, zero_idx - 5),3, puzzle))

    # excludes closed paths
    if closed != []:
        paths = set(paths)
        paths = [x for x in paths if x[0] not in closed[0]]

    return paths


# EXAMPLES 

# print(move('30142657',1,0)) # '03142657'

# print(find_possible_paths('30142657', [('32140617', 1)])) # [('32140657', 3, '30142657'), ('35142607', 3, '30142657'), ('36142057', 1, '30142657'), ('03142657', 1, '30142657'), ('31042657', 1, '30142657')]

# print(find_possible_paths('30142657')) # [('36142057', 1, '30142657'), ('03142657', 1, '30142657'), ('31042657', 1, '30142657'), ('35142607', 3, '30142657'), ('32140657', 3, '30142657')]
