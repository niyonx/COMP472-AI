"""
A* Algorithm (A*).
"""

import time, signal, traceback
from queue import PriorityQueue
from utils.HeuristicFunc import *
from utils.helper import *

def timeout_handler(signum, frame):
    raise Exception("timeout")

def astar(initial_puzzle: str, columns, rows, iteration_number, invoke_timeout=True, funcH = None):
    if(invoke_timeout):
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(TIMEOUT)

    # Create solution and search file
    sol, search = get_sol_file(f'_astar-{funcH.__name__}_', iteration_number), get_search_file(f'_astar-{funcH.__name__}_', iteration_number)

    try:
        start_time = time.time()
        initial_puzzle = puzzle(list(map(int, initial_puzzle.split())), columns, rows)
        initial_config = new_config(initial_puzzle, COST.ZERO, None, 0)
        search_length = 0

        CLOSED = [initial_config]

        OPEN = []
        OPEN = find_possible_paths(initial_puzzle, OPEN, closed = CLOSED, cumulative_cost=0, funcH = funcH)

        # Visits the initial configuration
        initial_config.calculateH(funcH)
        initial_config.calculateF()
        search.write(f"{initial_config.fValue} {initial_config.gValue} {initial_config.hValue} {initial_config.puzzle.to_string()}\n")

        while(OPEN):
            # Sort OPEN list by lowest h value (heuristic value)
            OPEN.sort(key=lambda x: x.fValue)

            # Traverse the shortest path first
            target = OPEN.pop(0)
            CLOSED.append(target)
            search_length += 1

            # Write visiting node to search file
            # Only write h(n) since gbfs does not use f(n) and g(n)
            search.write(f"{target.to_file(writeF = True, writeG = True, writeH = True)}\n")

            # Goal checking
            if(target.puzzle.is_win()):
                # Found the solution, stop the counter.
                signal.alarm(0)

                solution_path = []
                predecessor = target.predecessor
                total_cost = target.cost.value
                solution_path.append(CLOSED.pop(-1))

                # Backtracking to find solution path
                for config in reversed(CLOSED):
                    if(config.puzzle.is_equal(predecessor)):
                        predecessor = config.predecessor
                        solution_path.append(config)

                total_cost = solution_path[0].gValue

                duration = (time.time() - start_time)

                sol_length = -1
                for config in reversed(solution_path):
                    sol.write(
                        f"{config.to_file(write_to_solution = True)}\n"
                    )
                    sol_length += 1 

                # Total cost and time
                sol.write(f"{total_cost} {duration:.1f}")
                sol.close()
                search.close()

                return True, total_cost, duration, sol_length, search_length

            OPEN = find_possible_paths(target.puzzle, OPEN, CLOSED, cumulative_cost=target.gValue, funcH = funcH)

        return False, 0, 60, 0, search_length

    except Exception as exc:
        if(str(exc) == "timeout"):
            sol.write('no solution')
            sol.close()
            search.close()

            ## Reopens search file to delete contents
            search = get_search_file(f'_astar-{funcH.__name__}_', iteration_number)
            search.write('no solution')
            search.close()

            return False, 0, 60, 0, search_length

        print('Encountered exception (not timeout): ', exc)
        traceback.print_exc()

def run(puzzle_input = '', heuristicFunc = 0):
    print("Starting...")

    if(puzzle_input == ''):
        puzzle_input = INPUT_PATH

    files = open(puzzle_input, "r")
    puzzles = get_puzzles(puzzle_input)

    funcH = h0
    if(heuristicFunc == 1):
        funcH = h1
    if(heuristicFunc == 2):
        funcH = h2

    # Analysis
    sol_length = 0
    search_length = 0
    no_sol = 0
    cost = 0
    time = 0
    no_puzzles = len(puzzles)

    for number, puzzle in enumerate(puzzles):
        found_solution, total_cost, duration, total_sol_length, total_search_length = astar(puzzle, 4, 2, number, funcH = funcH)
        if (found_solution):
            print('Completed puzzle no.', number)
            print('Total cost: ', total_cost)
            print('Total solution length: ', total_sol_length)
            print('Total search length: ', total_search_length)
            print('Time: ', duration, ' milliseconds \n')
        else:
            no_sol += 1
            print('No solution for puzzle no.', number, '\n')
        
        sol_length += total_sol_length
        search_length += total_search_length
        cost += total_cost
        time += duration

    print('Finished!\n')

    print('Summary')
    print(f'\tSolution path total length: {sol_length}')
    print(f'\tSolution path average length: {(sol_length/ (no_puzzles-no_sol)):.2f}')
    print(f'\tSearch path total length: {search_length}')
    print(f'\tSearch path average length: {(search_length/ no_puzzles):.2f}')
    print(f'\tTotal no of no solution: {no_sol}')
    print(f'\tAverage no of no solution: {(no_sol/ no_puzzles):.2f}')
    print(f'\tTotal cost: {cost}')
    print(f'\tAverage cost: {(cost/ (no_puzzles-no_sol)):.2f}')
    print(f'\tTotal execution time: {time}')
    print(f'\tAverage execution time: {(time/no_puzzles):.2f}')
