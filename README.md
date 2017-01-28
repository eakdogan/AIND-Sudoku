# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Define a local naked twins constraint:
- Observe and define a local constraint for a unit: if two cells have exact same two candidates for a solution (naked twins), than no other cells in that unit can have those two digits as solution.
- Find all the naked twins in a unit
- Take a naked twin's candidate two digits
- Eliminate those two digits from other cells in the unit
- Apply same propagation (find naked twins and eliminate) to other units
- Repeat until we can not find any more naked twins in a unit

We use naked twins method in conjunction with elimination and only choice methods in sequence repeatedly until we arrive at an un-improvable board. If the board is still unsolved we now start simulating and employ search strategy to arrive at a solution.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We define a new diagonal units constraint for checking the peers in the elimination method:
- Create a new diagonal_units array
- Loop through rows and columns
- Add the box to the diagonal_units array if they are on one of the diagonals
- Add diagonal_units to the units array along with other units (square, rows, columns) so it can also be enforced as peers

We use naked twins method in conjunction with elimination and only choice methods in sequence repeatedly until we arrive at an un-improvable board. If the board is still unsolved we now start simulating and employ search strategy to arrive at a solution.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
