"""
Greedy Best First Search (gbfs).
"""

import time, signal, traceback
from utils.HeuristicFunc import *
from utils.helper import *

def timeout_handler(signum, frame):
    raise Exception("timeout")

def gbfs(initial_puzzle: str, columns, rows, iteration_number, invoke_timeout=True, funcH = None):
    if(invoke_timeout):
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(TIMEOUT)

    # Create solution and search file
    sol, search = get_sol_file('_gbfs_', iteration_number), get_search_file('_gbfs_', iteration_number)

    try:
        start_time = time.time()
        initial_puzzle = puzzle(list(map(int, initial_puzzle.split())), columns, rows)
        initial_config = new_config(initial_puzzle, COST.ZERO, None, 0)

        CLOSED = [initial_config]

        OPEN = []
        OPEN = find_possible_paths(initial_puzzle, OPEN, closed = CLOSED, cumulative_cost=0, funcH = funcH)

        # Visits the initial configuration
        initial_config.calculateH(funcH)
        search.write(f"0 0 {initial_config.hValue} {initial_config.puzzle.to_string()}\n")

        while(OPEN):
            # Sort OPEN list by lowest h value (heuristic value)
            OPEN.sort(key=lambda x: x.hValue)

            # Traverse the shortest path first
            target = OPEN.pop(0)
            CLOSED.append(target)

            # Write visiting node to search file
            # Only write h(n) since gbfs does not use f(n) and g(n)
            search.write(f"{target.to_file(writeH = True)}\n")

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
                        total_cost += config.cost.value
                        predecessor = config.predecessor
                        solution_path.append(config)

                duration = (time.time() - start_time)

                for config in reversed(solution_path):
                    sol.write(
                        f"{config.to_file(write_to_solution = True)}\n"
                    )

                # Total cost and time
                sol.write(f"{total_cost} {duration:.1f}")
                sol.close()
                search.close()

                return True, total_cost, duration

            OPEN = find_possible_paths(target.puzzle, OPEN, CLOSED, funcH = funcH)

        return False, -1, -1

    except Exception as exc:
        if(str(exc) == "timeout"):
            sol.write('no solution')
            sol.close()
            search.close()

            ## Reopens search file to delete contents
            search = get_search_file('_gbfs_', iteration_number)
            search.write('no solution')
            search.close()

            return False, -1, -1

        print('Encountered exception (not timeout): ', exc)
        traceback.print_exc()

def main():
    print("Starting...")

    files = open(INPUT_PATH, "r")
    puzzles = get_puzzles()

    for number, puzzle in enumerate(puzzles):
        found_solution, total_cost, duration = gbfs(puzzle, 4, 2, number, funcH = funcH1)
        if (found_solution):
            print('Completed puzzle no.', number)
            print('Total cost: ', total_cost)
            print('Time: ', duration, ' milliseconds \n')
        else:
            print('No solution for puzzle no.', number, '\n')

    print('Finished!')


if __name__ == "__main__":
    main()