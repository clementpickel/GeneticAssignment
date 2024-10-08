from sys import stderr
from typing import List

Genome = List[int]

def show_board(genome: Genome, board_size: int):
    board = [['.' for _ in range(board_size)]for _ in range(board_size)]
    for i in range(0, len(genome)):
        board[i][genome[i]] = 'Q'
    for line in board:
        for char in line:
            print(char, end=" ")
        print("")

def show_result(genome: Genome, generation: int, board_width: int, queens_number: int, fitness_score: int, time: float):
    print("result =", genome)
    print("generation =", generation)
    print("time =", time, "s")
    show_board(genome, board_width)
    combination = queens_number * (queens_number - 1) / 2
    if fitness_score != combination:
        print("Not a solution, generation limit reached, fitness =", fitness_score, "/", combination)

def is_num(str):
    try:
        int(str)
    except ValueError:
        exit(84)
    return int(str)

def help():
    print("""python3 main.py Q P L (M)
          Q = number of queens and board_width
          P = size of the population
          L = generation limit
          M = mutation chance, 0.1 by default""")
    
def input_check(queens_number: int, population: int, gen_lim: int):
    if queens_number < 4:
        print("Not enough queens", file=stderr)
        exit(84)
    if population < 2:
        print("Population too small", file=stderr)
        exit(84)
    if gen_lim < 1:
        print("Not enough generations", file=stderr)
        exit(84)
