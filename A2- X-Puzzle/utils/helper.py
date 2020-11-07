def move(puzzle, zero_idx, to_idx):
    if(zero_idx < to_idx):
        puzzle = puzzle[:zero_idx] + puzzle[to_idx] + puzzle[zero_idx+1:to_idx] + puzzle[zero_idx] + puzzle[to_idx+1:]
    else:
        puzzle = puzzle[:to_idx] + puzzle[zero_idx] + puzzle[to_idx+1:zero_idx] + puzzle[to_idx] + puzzle[zero_idx+1:]
    return puzzle

def find_possible_paths(puzzle, closed=[], columns=4, rows=2):
    # returns list of all possible paths in form (path, cost, predecessor, token_to_move)
    # TODO: when scaling, softcode values

    paths = []
    zero_idx = puzzle.index('0')
    last_idx = (columns*rows)-1
    

    # check move up
    if(zero_idx - columns >= 0):
        paths.append((move(puzzle, zero_idx, zero_idx - columns), 1, puzzle, zero_idx - columns))
    # check move down
    if(zero_idx + columns <= last_idx):
        paths.append((move(puzzle, zero_idx, zero_idx + columns), 1, puzzle, zero_idx + columns))
    # check move left
    if(zero_idx - 1 >= 0):
        if(zero_idx % columns != 0) # moving left might be illegal 12340567 to 12304567
            paths.append((move(puzzle, zero_idx, zero_idx - 1), 1, puzzle, zero_idx - 1))
    # check move right
    if(zero_idx + 1 <= last_idx):
        if((zero_idx + 1) % columns != 0) # moving right might be illegal 12304567 to 12340567
            paths.append((move(puzzle, zero_idx, zero_idx + 1), 1, puzzle, zero_idx + 1))
    # check move diag down-right
    if(zero_idx + (columns + 1) <= last_idx):
        paths.append((move(puzzle, zero_idx, zero_idx + (columns + 1)), 3, puzzle, zero_idx + (columns + 1)))
    # check move diag down-left
    if(zero_idx + (columns - 1) <= last_idx):
        # if zero_idx is in corner, diag move will lead to wrapping move e.g 01234567 to 31204567
        if(zero_idx % columns == 0 or (zero_idx + 1) % columns == 0): # left corner or right corner
            paths.append((move(puzzle, zero_idx, zero_idx + (columns - 1)), 2, puzzle, zero_idx + (columns - 1)))
        else:
            paths.append((move(puzzle, zero_idx, zero_idx + (columns - 1)), 3, puzzle, zero_idx + (columns - 1)))
    # check move diag up-right
    if(zero_idx - (columns - 1) >= 0):
        if(zero_idx % columns == 0 or (zero_idx + 1) % columns == 0): # left corner or right corner
            paths.append((move(puzzle, zero_idx, zero_idx - (columns - 1)), 2, puzzle, zero_idx - (columns - 1)))
        else:
            paths.append((move(puzzle, zero_idx, zero_idx - (columns - 1)), 3, puzzle,zero_idx - (columns - 1)))
    # check move diag up-left
    if(zero_idx - (columns + 1) >= 0):
        paths.append((move(puzzle, zero_idx, zero_idx - (columns + 1)), 3, puzzle, zero_idx - (columns + 1)))

    # excludes closed paths
    if closed != []:
        paths = set(paths)
        paths = [x for x in paths if x[0] not in closed[0]]

    return paths


# EXAMPLES 

# print(move('30142657',1,0)) # '03142657'

# print(find_possible_paths('30142657', [('32140617', 1)])) # [('32140657', 3, '30142657'), ('35142607', 3, '30142657'), ('36142057', 1, '30142657'), ('03142657', 1, '30142657'), ('31042657', 1, '30142657')]

# print(find_possible_paths('30142657')) # [('36142057', 1, '30142657'), ('03142657', 1, '30142657'), ('31042657', 1, '30142657'), ('35142607', 3, '30142657'), ('32140657', 3, '30142657')]
