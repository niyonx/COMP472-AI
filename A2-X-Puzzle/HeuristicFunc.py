from structure import *

"""
A naive heuristic h0 (not optimal)
"""
def funcH0(config: puzzle):
    if(config.content[config.last_idx] == 0):
        return 0
    return 1