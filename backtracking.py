import time
from sys import argv
from help import is_num

def is_safe(board, row, col, N):
    # Check this row on the left side
    for i in range(col):
        if board[row][i] == 1:
            return False

    # Check upper diagonal on the left side
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    # Check lower diagonal on the left side
    for i, j in zip(range(row, N, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    return True


def solve_n_queens_util(board, col, N):
    # Base case: If all queens are placed, return True
    if col >= N:
        return True

    # Try placing this queen in all rows one by one
    for i in range(N):
        if is_safe(board, i, col, N):
            # Place the queen
            board[i][col] = 1

            # Recur to place the rest of the queens
            if solve_n_queens_util(board, col + 1, N):
                return True

            # If placing queen in board[i][col] leads to a solution, return
            # Else, backtrack and remove the queen
            board[i][col] = 0

    # If the queen cannot be placed in any row in this column, return False
    return False


def solve_n_queens(N):
    # Initialize the chess board (N x N) with 0s
    board = [[0 for _ in range(N)] for _ in range(N)]

    # Start solving the problem using a utility function
    if not solve_n_queens_util(board, 0, N):
        print(f"No solution exists for {N} queens.")
        return None

    # If a solution is found, return the board
    return board


def print_solution(board):
    for row in board:
        print(" ".join("Q" if x == 1 else "." for x in row))

def main():
    if len(argv) != 2:
        print("""python3 backtracking.py N
        N = number of queens and width of the board""")
        exit(84)
    N = is_num(argv[1])
    start = time.time()
    solution = solve_n_queens(N)
    end = time.time()
    if solution:
        print("Solution found in", end-start, "s :")
        print_solution(solution)

main()