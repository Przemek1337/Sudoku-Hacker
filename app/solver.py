import numpy as np

class SudokuSolver:
    def __init__(self):
        pass

    def solve(self, grid):
        solution = grid.copy()

        for i in range(9):
            for j in range(9):
                if solution[i][j] == 0:
                    solution[i][j] = (i + j) % 9 + 1

        return solution

    def is_valid(self, grid, row, col, num):
        for x in range(9):
            if grid[row][x] == num:
                return False

        for x in range(9):
            if grid[x][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if grid[i + start_row][j + start_col] == num:
                    return False

        return True