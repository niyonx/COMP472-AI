import random

def generatePuzzle(columns, rows, number):
    filename = str(columns) + 'x' + str(rows) + '_' + str(number) + '_Puzzles.txt'
    file = open(filename, "w")
    possible_number = list(range(columns * rows))
    for i in range(number):
        random.shuffle(possible_number)
        file.write(' '.join(map(str, possible_number)))
        file.write('\n')
    file.close()
    print('Done writing to file: ', filename)

# Render 50 puzzles of size 5 x 5
generatePuzzle(5, 5, 50)