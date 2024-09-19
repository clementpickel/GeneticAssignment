import itertools
import time
from sys import argv
from help import is_num

def is_valid(board):
    N = len(board)
    
    # Check each pair of queens
    for i in range(N):
        for j in range(i + 1, N):
            # Check if queens are on the same row, same column or same diagonal
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                return False
    return True

def solve_n_queens_brute_force(N):
    # Generate all permutations of positions for N queens
    all_permutations = itertools.permutations(range(N))
    
    # Check each permutation if it's a valid solution
    for perm in all_permutations:
        if is_valid(perm):
            return perm
    return None

def print_solution(solution):
    N = len(solution)
    for i in range(N):
        row = ['.'] * N
        row[solution[i]] = 'Q'
        print(" ".join(row))

def main():
    if len(argv) != 2:
        print("""python3 bruteforce.py N
        N = number of queens and width of the board""")
        exit(84)
    N = is_num(argv[1])
    start = time.time()
    solution = solve_n_queens_brute_force(N)
    end = time.time()
    if solution:
        print("Solution found in", end-start, "s :")
        print_solution(solution)

main()