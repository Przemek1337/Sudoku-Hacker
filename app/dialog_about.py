import tkinter as tk

def show_about_dialog(parent, controller):
    about_window = tk.Toplevel(parent)
    about_window.title("O aplikacji")
    about_window.geometry("600x400")
    about_window.configure(bg=controller.background_color)

    header = tk.Frame(about_window, bg=controller.accent_color, padx=15, pady=10)
    header.pack(fill="x")

    title = tk.Label(header, text="O aplikacji AI Sudoku Solver",
                     font=("Helvetica", 16, "bold"),
                     bg=controller.accent_color, fg="white")
    title.pack()

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
    about_label = tk.Label(content, text=about_text,
                                 font=("Helvetica", 11),
                                 bg=controller.background_color, fg=controller.text_color,
                                 justify="left")
    about_label.pack(pady=10)

    close_btn = tk.Button(content, text="Zamknij",
                          command=about_window.destroy,
                          font=("Helvetica", 12),
                          bg=controller.button_color,
                          fg="white",
                          padx=10, pady=5)
    close_btn.pack(pady=15)