from structure import *

"""
A naive heuristic h0 (not optimal)
"""
def funcH0(config: puzzle):
    if(config.content[config.last_idx] == 0):
        return 0
    return 1

def funcH1(config: puzzle):
    max_count = 0
    count = 0
    for win in WIN_CONFIG:
        for i, data in enumerate(win):
            if(config.content[i] == data):
                count += 1
        if(max_count < count):
            max_count = count
        count = 0
    return (config.columns * config.rows) - max_count

# print(funcH1(puzzle([1,2,3,4,7,6,5,0],4,2)))