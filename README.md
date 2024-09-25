# GeneticAssignment

This project implements a genetic algorithm to solve various problems such as the N-Queens problem, Traveling Salesman Problem (TSP), or any similar optimization problem. The genome representation in this case is defined as `[Y, ...]` for each queen on the board, where each Y denotes the position of a queen on the chessboard and it's index in the list is it's X.

## Requirements

- **Python 3.x**

### For test.py

- **Pillow**
- **Matplotlib**

```bash
pip install pillow
pip install maplotlib
```

## How to Run

To run the genetic algorithm:

```bash
python3 main.py -h
python3 main.py B Q P L (M)
      B = board width
      Q = number of queens
      P = size of the population
      L = generation limit
      M = mutation chance, 0.1 by default
```

To compare our genetic algorithm to other methods of solving the N-queens problem we add a bruteforce ans a backtracking algorithm

```bash
python3 bruteforce.py N
      N = number of queens and width of the board
```

```bash
python3 backtracking.py N
      N = number of queens and width of the board
```

To test our genetic algorithm and generate a graph you can edit test.py and launch it

```bash
python3 test.py
```

## Problem Details

### Genome Representation

For the N-Queens problem, each genome is represented as a list of `[X, Y]` pairs, where:

- `X` is the row number.
- `Y` is the column number.
  Each pair corresponds to the position of one queen on the board.

### Genetic Algorithm Overview

1. **Initial Representation**: Initially, the genome was represented as binary positions of queens on the board.
2. **Current Representation**: The genome now consists of the actual positions of queens on the board in the form of `[X, Y]` coordinates, allowing easier representation and fitness evaluation.

### Fitness Function

- The fitness function initially counted the number of non-attacking queens. However, this was later updated to count the number of **non-attacking pairs** of queens. The goal is to maximize the number of non-attacking pairs, ensuring a valid solution to the N-Queens problem.

### Mutation Strategy

- Initially, the mutation involved adding or subtracting 1 from a queen's position.
- This was changed to randomly selecting a position between 0 and the board size, providing a more flexible and effective mutation strategy for the genetic algorithm.

## Sources

- [Genetic Algorithms Explained By Example](https://www.youtube.com/watch?v=uQj5UNhCPuo)
- [Genetic Algorithm from Scratch in Python (tutorial with code)](https://www.youtube.com/watch?v=nhT56blfRpE)
- [Checking for horizontal, vertical and diagonal pairs given coordinates](https://stackoverflow.com/questions/41432956/checking-for-horizontal-vertical-and-diagonal-pairs-given-coordinates)
- [Solving the 8-Queens Problem using Genetic Algorithm](https://www.educative.io/answers/solving-the-8-queen-problem-using-genetic-algorithm)

## Overleaf report

[Overleaf report](https://www.overleaf.com/read/yrdgkhtvqkqp#38da64)

## Steps Taken

1. Changed genome representation from binary positions to `[X, Y]` coordinates for more intuitive handling of queen positions.
2. The genetic algorithm was refined to handle scenarios where multiple queens could occupy the same position, ensuring that convergence happens without conflicts.
3. The fitness function was updated from simply counting non-attacking queens to counting **non-attacking pairs**, focusing on pairwise comparisons.
4. Mutation was improved by changing the approach from incremental mutation (`+/- 1`) to a random mutation within the range `[0, board_size]` for more effective exploration of the solution space.

## GitHub Repository

You can find the full project and code at the following GitHub repository:

[GeneticAssignment GitHub Repository](https://github.com/clementpickel/GeneticAssignment)
