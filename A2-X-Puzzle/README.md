## X-Puzzle

### Project Structure

```
A2-X-Puzzle
│   README.md
│   AStar.py
│   GreedyBestFirstSearch.py
│   UniformCostSearch.py
│   cli.py
│
│   SamplePuzzle.txt
│
└───utils
│   │   helper.py
│   │   HeuristicFunc.py
│   │   structure.py
│
│
└───output
    │   0_astar-h0_search.txt
    │   0_astar-h0_solution.txt
    │   ...
```

### CLI to run search algorithms:

+ `python3 cli.py run`: The cli will prompt for inputs (or user can specify the options as command line arguments)
    - `python3 cli.py run --help`: for help
    - `Run Algotithm:`
        + `ucs`: Uniform Cost Search
        + `gbfs`: Greedy Best First Search
        + `astar`: A Star
    - `-h`: 3 options: 0, 1, 2 represents h0, h1, h2 respectively
    - `path`: The path to the input puzzle. `SamplePuzzle.txt` by default

+ `python3 cli.py clean` to clean the output directory. (without deleting the directory).