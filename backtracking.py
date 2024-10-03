import time
from sys import argv
from help import is_num

def is_safe(board, row, col, N):
    for i in range(col):
        if board[row][i] == 1:
            return False

    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    for i, j in zip(range(row, N, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    return True


def solve_n_queens_util(board, col, N):
    if col >= N:
        return True

    for i in range(N):
        if is_safe(board, i, col, N):
            board[i][col] = 1

            if solve_n_queens_util(board, col + 1, N):
                return True

            board[i][col] = 0

    return False


def solve_n_queens(N):
    board = [[0 for _ in range(N)] for _ in range(N)]

    if not solve_n_queens_util(board, 0, N):
        print(f"No solution exists for {N} queens.")
        return None

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