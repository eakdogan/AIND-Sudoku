assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

print('....starting the algorithm....') #for debugging
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[],[]] #used for diagonal sudokus
for i in range(len(rows)):
    "Iterate through the rows and columns simultaneously to create the two diagonal units."
    r1 = rows[i]
    r2 = rows[len(rows)-1-i]
    c = cols[i]
    diagonal_units[0].append(r1+c)
    diagonal_units[1].append(r2+c)
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
        # Eliminate the naked twins as possibilities for their peers
    stalled = False
    while not stalled:
        len_values_before = [len(v) for v in values.values()] #compare the candidate counts for each cell to see if we are making progress
        for unit in unitlist: #Loop through units and elimiate since naked twins makes sense only in unit context
            tuples = [box for box in unit if len(values[box]) == 2] #find all cells with 2 digit candidates
            if len(tuples)>1: #if there's only a single cell with two candidates, there can not be naked twins
                for box1 in tuples: #loop through the two digit cells in the unit and
                    for box2 in tuples: #compare each cell against other cells with two digits in same unit to find naked twins
                        if box1 != box2 and values[box1] == values[box2] : #we got a match of digits -> A Naked Twin
                                for box3 in unit:   #loop through the unit and remove the twin values from other cells
                                    if len(values[box3])>=2 and values[box3] != values[box1] and len(values[box1])==2: # do not remove values from naked twins
                                        #print('removing'+values[box1][0]+values[box1][1]+' in '+values[box3]) #for debugging
                                        values[box3] = values[box3].replace(values[box1][0],'')
                                        values[box3] = values[box3].replace(values[box1][1],'')
        len_values_after = [len(v) for v in values.values()]
        stalled = len_values_before == len_values_after
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate(), only_choice() and naked twins. If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many candidates each box have
        len_values_before = len([box for box in values.values() ])
        #employ eliminate strategy
        values = eliminate(values)
        #employ only choice strategy
        values = only_choice(values)
        #employ naked twins strategy
        values = naked_twins(values)
        #compare to see if we made progress
        len_values_after = len([box for box in values.values() ])
        stalled = len_values_before == len_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the elimination, only choice and naked twins
    values = reduce_puzzle(values)
    #print('....starting search....') #for debugging
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid, diagonal=True):
    """
    Diagonal parameter should be passed as False for solving non-diagonal puzzles
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    #First remove the diagonal units from unitlist for non-diagonal puzzles
    global row_units
    global column_units
    global square_units
    global unitlist
    global units
    global peers
    if diagonal == False:
        unitlist =  row_units + column_units + square_units  #do not include diagonals as units for checking
        units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
        peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

    values = grid_values(grid)
    return search(values)  #reduces until un-reducable and that searches

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    test =             '.47.8...1............6..7..6....357......5....1..6....28..4.....9.1...4.....2.69.'
    test =             '3...8.......7....51..............36...2..4....7...........6.13..452...........8..'
    test =             '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    test =             '.5..9....1.....6.....3.8.....8.4...9514.......3....2..........4.8...6..77..15..6.'
    #worlds hardest sudoku puzzle below. solves OK:
    test =             '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'

    display(solve(diag_sudoku_grid))
    #try below for test cases
    #display(solve(test,False))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
