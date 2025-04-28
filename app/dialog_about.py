import tkinter as tk

def show_about_dialog(parent, controller):
    about_window = tk.Toplevel(parent)
    about_window.title("O aplikacji")
    about_window.geometry("600x400")
    about_window.configure(bg=controller.background_color)

    # Header
    header = tk.Frame(about_window, bg=controller.accent_color, padx=15, pady=10)
    header.pack(fill="x")

    title = tk.Label(header, text="O aplikacji AI Sudoku Solver",
                     font=("Helvetica", 16, "bold"),
                     bg=controller.accent_color, fg="white")
    title.pack()

    # Content
    content = tk.Frame(about_window, bg=controller.background_color, padx=20, pady=20)
    content.pack(fill="both", expand=True)

    about_text = """
    Sudoku Solver to aplikacja wykorzystująca 
    sztuczną inteligencję do rozwiązywania łamigłówek Sudoku.

    Program potrafi:
    - Analizować obrazy planszy Sudoku
    - Rozpoznawać cyfry
    - Rozwiązywać łamigłówki Sudoku
    """