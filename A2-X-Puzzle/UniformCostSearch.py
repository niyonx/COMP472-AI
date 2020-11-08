import time, signal
from utils import helper

file = open(helper.INPUT_PATH, "r")
puzzles = helper.get_puzzles()

def timeout_handler(signum, frame):
    raise Exception("timeout")

def ucs(puzzle: str, number, invokeTimeout = True):
    if(invokeTimeout):
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(helper.TIMEOUT)
    
    # Create solution and search file
    sol, search = helper.get_sol_search_files('_ucs_', number)

    try:
        startTime = time.time()

        initial = puzzle

        cost = 0
        totalCost = 0

        closed = []
        opened = helper.find_possible_paths(puzzle)

        while(opened):
            opened.sort(key=lambda x: x[1].value)
            puzzle, cost, predecessor, token_to_move = opened.pop(0)
            closed.append((puzzle, cost, predecessor, token_to_move))

            # Goal checking
            if (puzzle in helper.WIN_CONFIG):
                # Found the solution, stop the counter
                signal.alarm(0)

                path = []
                predecessor = closed[-1][2]
                totalCost += closed[-1][1].value
                path.append(closed.pop(-1))

                # Backtracking to find solution path
                for puzzle in reversed(closed):
                    if(puzzle[0] == predecessor):
                        totalCost += puzzle[1].value
                        predecessor = puzzle[2]
                        path.append(puzzle)

                duration = (time.time() - startTime)
                # Write intial configuration
                sol.write(f"0 0 {' '.join(initial)}\n")
                for puzzle in reversed(path):
                    sol.write(f"{puzzle[3]} {puzzle[1].value} {' '.join(puzzle[0])}\n")
                    # Each line starts with '0 0 0' because UCS does not use heuristic 
                    search.write(f'0 0 0 {" ".join(puzzle[0])}\n')
            
                # Total cost and time
                sol.write(f"{totalCost} {duration:.1f}")
                sol.close()
                search.close()
                return True

            opened.extend(helper.find_possible_paths(puzzle, closed))
        
    except Exception as exc:
        if ( str(exc) == "timeout"):            
            sol.write('no solution')
            sol.close()
            search.write('no solution')
            search.close()
            return False
        print('Encountered oher exception (not timeout): ', exc)

def main():
    print("Starting...")
    for number, puzzle in enumerate(puzzles):
        if (ucs(puzzle, number)):
            print('Completed puzzle no.', number)
        else:
            print('No solution for puzzle no.', number)

    print('Finished!')

if __name__ == "__main__":
    main()