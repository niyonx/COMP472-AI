"""
The CLI
"""
import click
import os, shutil
import GreedyBestFirstSearch
import AStar
import UniformCostSearch

@click.group()
def main():
   pass

@main.command()
@click.option('--path', prompt='Path to output folder', default='./output', help='The path to output folder, default to ./output ')
def clean(path):
    click.echo('Cleaning output folder. (deleting the files only)')
    shutil.rmtree(path)
    os.mkdir(path)
    click.echo('Done!')

@main.command()
@click.option('--algo', prompt='Run algorithm ',
              help='Type of algorithm to run.(ucs, gbfs, astar)')
@click.option('--h', prompt='Type of heuristic function (will be ignored if it is ucs)', default=0, help='Type of heuristic function (h0, h1, h2). If the choosen algorithm is UCS, ignore this.')
@click.option('--path', default='', help='The path to the input puzzles. SamplePuzzle.txt by default')
def run(algo, h, path):
    if (h not in [0, 1, 2]):
        click.echo('Invalid number of heuristic function. See --help')
        return
    if(algo == 'ucs'):
        UniformCostSearch.run(path)
    elif (algo == 'gbfs'):
        GreedyBestFirstSearch.run(path, h)
    elif (algo == 'astar'):
        AStar.run(path, h)
    else:
        click.echo('Invalid syntax. See --help')
        return


if __name__ == '__main__':
    main()