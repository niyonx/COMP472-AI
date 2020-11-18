from utils.structure import *
from bisect import bisect_left

"""
A naive heuristic h0 (not optimal)
"""
def h0(config: puzzle):
    if(config.content[config.last_idx] == 0):
        return 0
    return 1

# Counts misplaced tiles
def h1(config: puzzle):
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

'''
A heuristic function that is a combination of Manhattan distance and linear conflicts heuristics.
'''
def h2(config:puzzle):
    return ( manhattan_distance(config) + linear_conflicts(config) ) / 2


def manhattan_distance(config: puzzle):
    def get_distance(have, want, columns):
        distance = 0
        for i in range(len(have)):
            target = have[i]
            if(target):
                suppose_idx = want.index(target)
                distance += abs(i % columns - suppose_idx % columns) + abs(i // columns - suppose_idx // columns)
        return distance

    hValues = []
    for win in WIN_CONFIG:
        hValues.append(get_distance(config.content, win, config.columns))

    return sum(hValues) / len(hValues)


def linear_conflicts(config: puzzle):
    # Count linear conflicts for a row
    def count_conflicts(have, want, columns):
        inversion = 0
        for i in range(columns):
            if(have[i] != 0):
                iPos = bisect_left(want, have[i])
                if(0 <= iPos):
                    for j in range(i):
                        if(have[j] != 0):
                            jPos = bisect_left(want, have[j])
                            if(0 <= jPos):
                                if((have[i] < have[j]) != (i < j)):
                                    inversion += 1
        return inversion

    hValues = []
    for win in WIN_CONFIG:
        j = 0
        count = 0
        for i in range(config.rows):
            count += count_conflicts(\
                [x for x in config.content[j:(j + config.columns)]],\
                [x for x in win[j:(j + config.columns)]],\
                config.columns )
            j += config.columns

        hValues.append(count)

    return sum(hValues) / len(hValues)
