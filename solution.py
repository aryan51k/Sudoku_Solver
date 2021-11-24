from utils import *
import time

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)
print(square_units)


def eliminate(values):
    solved_boxes = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_boxes:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def naked_twins(values):
    for i in unitlist:
        box_values = [values[box] for box in i]
        naked_twins_value = []
        for j in box_values:
            if box_values.count(j) == 2 and len(j) == 2:
                naked_twins_value.append(j)

        for box in i:
            if values[box] in naked_twins_value:
                continue
            for twin in naked_twins_value:
                for digit in twin:
                    values[box] = values[box].replace(digit, '')

    return values


def only_choice(values):
    for unit in unitlist:
        for digit in cols:
            can_place_digit = []
            for place in unit:
                if digit in values[place]:
                    can_place_digit.append(place)

            if len(can_place_digit) == 1:
                values[can_place_digit[0]] = digit

    return values


def solved_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        if solved_values_before == solved_values_after:
            stalled = True
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values


def search(values):
    flag = 0
    values = solved_puzzle(values)
    if not values:
        print('Sorry solution cannot be found')
        return False

    for i in boxes:

        flag = 0

        if len(values[i]) != 1:
            flag = 0
        else:
            flag = 1

    if flag == 1:
        print('Solution Found ')
        return values

    remaining_values_min = [(len(values[b]), b) for b in boxes if len(values[b]) > 1]
    min_val = min(remaining_values_min, key=lambda x: x[0])
    to_solve_backtracking_on = min_val[1]
    for i in values[to_solve_backtracking_on]:
        sudoku = values.copy()
        sudoku[to_solve_backtracking_on] = i
        attempt = search(sudoku)
        if attempt:
            return attempt


def solve(grid):
    values = grid2values(grid)
    st = time.time()
    values = search(values)
    print(time.time() - st)
    display(values)
    return values


# diag_sudoku_grid = '5.1...4...9.6...1.2...3..7.........1...1..6.2.8...5.3.....9...4.64..32...........'
diag_sudoku_grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
# diag_sudoku_grid = '53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79'
# diag_sudoku_grid = '..9..6.2......759..84....7.1...5...6......9...7.1.3....9..........56...2..1.2....'
result = solve(diag_sudoku_grid)
