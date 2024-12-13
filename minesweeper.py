"""
A command line version of Minesweeper

Base Minesweeper game created by @Mohd-akram
https://gist.github.com/mohd-akram/3057736#file-minesweeper-py
"""
import random
import re
import time
from string import ascii_lowercase


def setupgrid(gridsize, start, numberofmines):
    emptygrid = [['0' for i in range(gridsize)] for i in range(gridsize)]

    mines = getmines(emptygrid, start, numberofmines)

    for i, j in mines:
        emptygrid[i][j] = 'X'

    grid = getnumbers(emptygrid)

    return (grid, mines)


def showgrid(grid):
    gridsize = len(grid)

    horizontal = '   ' + (4 * gridsize * '-') + '-'

    # Print top column letters
    toplabel = '     '

    for i in ascii_lowercase[:gridsize]:
        toplabel = toplabel + i + '   '

    print(toplabel + '\n' + horizontal)

    # Print left row numbers
    for idx, i in enumerate(grid):
        row = '{0:2} |'.format(idx + 1)

        for j in i:
            row = row + ' ' + j + ' |'

        print(row + '\n' + horizontal)

    print('')


def getrandomcell(grid):
    gridsize = len(grid)

    a = random.randint(0, gridsize - 1)
    b = random.randint(0, gridsize - 1)

    return (a, b)


def getneighbors(grid, rowno, colno):
    gridsize = len(grid)
    neighbors = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            elif -1 < (rowno + i) < gridsize and -1 < (colno + j) < gridsize:
                neighbors.append((rowno + i, colno + j))

    return neighbors


def getmines(grid, start, numberofmines):
    mines = []
    neighbors = getneighbors(grid, *start)

    for i in range(numberofmines):
        cell = getrandomcell(grid)
        while cell == start or cell in mines or cell in neighbors:
            cell = getrandomcell(grid)
        mines.append(cell)

    return mines


def getnumbers(grid):
    for rowno, row in enumerate(grid):
        for colno, cell in enumerate(row):
            if cell != 'X':
                # Gets the values of the neighbors
                values = [grid[r][c] for r, c in getneighbors(grid,
                                                              rowno, colno)]

                # Counts how many are mines
                grid[rowno][colno] = str(values.count('X'))

    return grid


def showcells(grid, currgrid, rowno, colno):
    # Exit function if the cell was already shown
    if currgrid[rowno][colno] != ' ':
        return

    # Show current cell
    currgrid[rowno][colno] = grid[rowno][colno]

    # Get the neighbors if the cell is empty
    if grid[rowno][colno] == '0':
        for r, c in getneighbors(grid, rowno, colno):
            # Repeat function for each neighbor that doesn't have a flag
            if currgrid[r][c] != 'F':
                showcells(grid, currgrid, r, c)


def playagain():
    choice = input('Play again? (y/n): ')

    return choice.lower() == 'y'


def parseinput(inputstring, gridsize, helpmessage):
    cell = ()
    flag = False
    message = "Invalid cell. " + helpmessage

    pattern = r'([a-{}])([0-9]+)(f?)'.format(ascii_lowercase[gridsize - 1])
    validinput = re.match(pattern, inputstring)

    if inputstring == 'help':
        message = helpmessage

    elif validinput:
        rowno = int(validinput.group(2)) - 1
        colno = ascii_lowercase.index(validinput.group(1))
        flag = bool(validinput.group(3))

        if -1 < rowno < gridsize:
            cell = (rowno, colno)
            message = ''

    return {'cell': cell, 'flag': flag, 'message': message}


def get_cell_mine_count(grid, rowno, colno):
    if rowno < 0 or rowno >= len(grid) or colno < 0 or colno >= len(grid[0]):
        raise ValueError("Cell position is out of bounds.")

    neighbors = getneighbors(grid, rowno, colno)

    mine_count = sum(1 for r, c in neighbors if grid[r][c] == 'X')

    return mine_count


def click_tile(grid, currgrid, rowno, colno):
    if rowno < 0 or rowno >= len(grid) or colno < 0 or colno >= len(grid[0]):
        raise ValueError("Tile position is out of bounds.")

    currcell = currgrid[rowno][colno]

    if grid[rowno][colno] == 'X':
        raise ValueError("Game Over: You clicked on a mine!")

    if currcell == ' ':
        showcells(grid, currgrid, rowno, colno)
    else:
        print("Already clicked on this tile")


def playgame():
    gridsize = 9
    numberofmines = 10

    currgrid = [[' ' for i in range(gridsize)] for i in range(gridsize)]

    grid = []
    flags = []
    starttime = 0

    helpmessage = ("Type the column followed by the row (eg. a5). "
                   "To put or remove a flag, add 'f' to the cell (eg. a5f).")

    showgrid(currgrid)
    print(helpmessage + " Type 'help' to show this message again.\n")

    while True:
        minesleft = numberofmines - len(flags)
        prompt = input('Enter the cell ({} mines left): '.format(minesleft))
        result = parseinput(prompt, gridsize, helpmessage + '\n')

        message = result['message']
        cell = result['cell']

        if cell:
            print('\n\n')
            rowno, colno = cell
            currcell = currgrid[rowno][colno]
            flag = result['flag']

            if not grid:
                grid, mines = setupgrid(gridsize, cell, numberofmines)
            if not starttime:
                starttime = time.time()

            if flag:
                # Add a flag if the cell is empty
                if currcell == ' ':
                    currgrid[rowno][colno] = 'F'
                    flags.append(cell)
                # Remove the flag if there is one
                elif currcell == 'F':
                    currgrid[rowno][colno] = ' '
                    flags.remove(cell)
                else:
                    message = 'Cannot put a flag there'

            # If there is a flag there, show a message
            elif cell in flags:
                message = 'There is a flag there'

            elif grid[rowno][colno] == 'X':
                print('Game Over\n')
                showgrid(grid)
                if playagain():
                    playgame()
                return

            elif currcell == ' ':
                showcells(grid, currgrid, rowno, colno)

            else:
                message = "That cell is already shown"

            if set(flags) == set(mines):
                minutes, seconds = divmod(int(time.time() - starttime), 60)
                print(
                    'You Win. '
                    'It took you {} minutes and {} seconds.\n'.format(minutes,
                                                                      seconds))
                showgrid(grid)
                if playagain():
                    playgame()
                return

        showgrid(currgrid)
        print(message)


#playgame()


# Alternate main
# def playgame_with_ai(ai_agent):
#     gridsize = 9
#     numberofmines = 10

#     currgrid = [[' ' for _ in range(gridsize)] for _ in range(gridsize)]

#     grid = []
#     flags = []
#     starttime = 0

#     showgrid(currgrid)

#     while True:
#         minesleft = numberofmines - len(flags)
#         print(f'AI is making a move... ({minesleft} mines left)')

#         result = ai_agent(grid, currgrid, flags)
#         rowno, colno = result['cell']
#         flag = result.get('flag', False)

#         currcell = currgrid[rowno][colno]

#         if not grid:
#             grid, mines = setupgrid(gridsize, (rowno, colno), numberofmines)
#         if not starttime:
#             starttime = time.time()

#         if flag:
#             if currcell == ' ':
#                 currgrid[rowno][colno] = 'F'
#                 flags.append((rowno, colno))
#             elif currcell == 'F':
#                 currgrid[rowno][colno] = ' '
#                 flags.remove((rowno, colno))
#             else:
#                 print('Cannot put a flag there')

#         elif (rowno, colno) in flags:
#             print('There is a flag there')

#         elif grid[rowno][colno] == 'X':
#             print('Game Over\n')
#             showgrid(grid)
#             if playagain():
#                 playgame_with_ai(ai_agent)
#             return

#         elif currcell == ' ':
#             showcells(grid, currgrid, rowno, colno)

#         else:
#             print("That cell is already shown")

#         if set(flags) == set(mines):
#             minutes, seconds = divmod(int(time.time() - starttime), 60)
#             print(
#                 f'You Win. It took you {minutes} minutes and {seconds} seconds.\n')
#             showgrid(grid)
#             if playagain():
#                 playgame_with_ai(ai_agent)
#             return

#         showgrid(currgrid)


# def dummy_ai_agent(grid, currgrid, flags): # TODO
#     for row in range(len(currgrid)):
#         for col in range(len(currgrid[row])):
#             if currgrid[row][col] == ' ' and (row, col) not in flags:
#                 return {'cell': (row, col), 'flag': False}

def collect_constraints(grid) :

    rules_related_to_tile = {}
    rules = {}

    for i in range(len(grid)) :
        for j in range(len(grid[i])) :
            rules_related_to_tile[(i, j)] = []

    for i in range(len(grid)) :
        for j in range(len(grid[i])) :
            if grid[i][j] != ' ' :
                rule = (set(), grid[i][j])
                for i1 in range(i-1, i+2) :
                    if i1 >= 0 and i1 < len(grid) :
                        for j1 in range(j-1, j+2) :
                            if j1 >= 0 and j1 < len(grid[i]) :
                                if grid[i1][j1] == ' ' :
                                    rule[0].add((i1, j1))
                rules[(i, j)] = rule
                for k in rule[0] :
                    rules_related_to_tile[k].append(rule)

    return rules_related_to_tile, rules

def is_subset(r1, r2) :
    return r1[0].issubset(r2[0])

def intersection(s1, s2) :
    return s1.difference(s2)

def remove_tile_from_rules(rules_by_tile, tile, rule, is_mine) :
    for r in rules_by_tile[tile] :
        if r != rule :
            print("Pre-Transform: ", r, is_mine)
            tiles = r[0]
            tiles.discard(tile)
            r = (tiles, r[1] - 1 if is_mine else r[1])
            print("Post-Transform: ", r)
    rules_by_tile[tile] = []

def csp_ai_agent(grid) :

    rules_by_tile, rules = collect_constraints(grid)
    new_rules = []
    
    queue = []
    mines = []
    safe = []

    for tile, rule in rules.items() :
        queue.append((tile, rule))

    while (len(queue) != 0) :
        tile, rule = queue.pop(0)
        if rule[1] == 0 :
            for t in rule[0] :
                safe.append(t)
                remove_tile_from_rules(rules_by_tile, t, rule, False)
        if rule[1] == len(rule[0]) :
            for t in rule[0] :
                mines.append(t)
                remove_tile_from_rules(rules_by_tile, t, rule, True)
        for r in rules_by_tile[tile] :
            if (r != rule and is_subset(r, rule)) :
                new_rule = (intersection(r[0], rule[0]), r[1] - rule[1])
                new_rules.append(new_rule)
                for t in new_rule[0] :
                    rules_by_tile[t].append(new_rule)
                    for r1 in rules_by_tile[t] :
                        queue.append(r1)

    print(safe, mines)

gridsize = 10

currgrid = [[' ' for i in range(gridsize)] for i in range(gridsize)]

currgrid[0][0] = 2
currgrid[0][1] = 2
currgrid[0][2] = 3

csp_ai_agent(currgrid)