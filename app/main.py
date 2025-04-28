import tkinter as tk
from app_gui import SudokuSolverApp
from solver import SudokuSolver
from model_handler import ModelHandler

def main():
    root = tk.Tk()
    model_handler = ModelHandler()

    solver = SudokuSolver()

    app = SudokuSolverApp(root, model_handler, solver)
    root.mainloop()

if __name__ == "__main__":
    main()
