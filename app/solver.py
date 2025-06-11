class SudokuSolver:
    def __init__(self):
        pass

    def solve(self, grid):
        """
        Rozwiązuje Sudoku używając algorytmu backtracking
        """

        if not self.is_valid_initial_state(grid):
            print("Błąd: Wejściowe Sudoku zawiera błędy!")
            return grid

        solution = [row[:] for row in grid]

        if self.solve_backtrack(solution):
            return solution
        else:
            print("Nie można rozwiązać tego Sudoku!")
            return grid

    def solve_backtrack(self, grid):
        """
        Rekurencyjne rozwiązywanie używając backtracking
        """
        # Znajdź następne puste pole
        empty_cell = self.find_empty_cell(grid)
        if not empty_cell:
            return True

        row, col = empty_cell

        for num in range(1, 10):
            if self.is_valid(grid, row, col, num):
                grid[row][col] = num

                if self.solve_backtrack(grid):
                    return True

                grid[row][col] = 0

        return False  # Żadna liczba nie działa

    def find_empty_cell(self, grid):
        """
        Znajduje pierwsze puste pole (z wartością 0)
        """
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, grid, row, col, num):
        """
        Sprawdza czy liczba może być umieszczona w danym miejscu
        """

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

    def is_complete(self, grid):
        """
        Sprawdza czy Sudoku jest kompletnie i poprawnie rozwiązane
        """
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return False
                if not self.is_valid_placement(grid, i, j):
                    return False
        return True

    def is_valid_placement(self, grid, row, col):
        """
        Sprawdza czy aktualna liczba w danym miejscu jest poprawna
        """
        num = grid[row][col]
        if num == 0:
            return True

        grid[row][col] = 0
        valid = self.is_valid(grid, row, col, num)
        grid[row][col] = num

        return valid

    def is_valid_initial_state(self, grid):
        """
        Sprawdza czy wejściowe Sudoku nie zawiera błędów
        """
        print("=== SPRAWDZANIE WEJŚCIOWEJ PLANSZY ===")
        self.print_grid(grid)

        conflicts = []
        for i in range(9):
            for j in range(9):
                if grid[i][j] != 0:
                    if not self.is_valid_placement(grid, i, j):
                        conflicts.append(f"Konflikt na pozycji ({i},{j}) = {grid[i][j]}")

        if conflicts:
            print("ZNALEZIONE KONFLIKTY:")
            for conflict in conflicts:
                print(f"  - {conflict}")
            return False

        print("Plansza wejściowa jest poprawna!")
        return True

    def print_grid(self, grid):
        """
        Wyświetla planszę w czytelnym formacie (pomocne do debugowania)
        """
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("------+-------+------")
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")
                if grid[i][j] == 0:
                    print(". ", end="")
                else:
                    print(str(grid[i][j]) + " ", end="")
            print()