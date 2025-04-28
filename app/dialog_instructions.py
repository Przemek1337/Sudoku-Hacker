import tkinter as tk

def show_instructions_dialog(parent, controller):
    instruction_window = tk.Toplevel(parent)
    instruction_window.title("Instrukcja obsługi")
    instruction_window.geometry("600x400")
    instruction_window.configure(bg=controller.background_color)

    # Header
    header = tk.Frame(instruction_window, bg=controller.accent_color, padx=15, pady=10)
    header.pack(fill="x")

    title = tk.Label(header, text="Instrukcja obsługi programu",
                     font=("Helvetica", 16, "bold"),
                     bg=controller.accent_color, fg="white")
    title.pack()

    # Content
    content = tk.Frame(instruction_window, bg=controller.background_color, padx=20, pady=20)
    content.pack(fill="both", expand=True)

    instructions_text = """
    Jak korzystać z aplikacji Sudoku Solver:

    1. Na stronie głównej kliknij przycisk "Rozpocznij".

    2. Na ekranie rozwiązywania Sudoku kliknij "Wczytaj obraz" i wybierz 
       zdjęcie planszy Sudoku z Twojego komputera.

    3. Po wczytaniu obrazu kliknij "Rozwiąż Sudoku".

    4. Program rozpozna planszę i rozwiąże Sudoku, 
       wyświetlając wykrytą macierz i rozwiązanie.
    """

    instruction_label = tk.Label(content, text=instructions_text,
                                 font=("Helvetica", 11),
                                 bg=controller.background_color, fg=controller.text_color,
                                 justify="left")
    instruction_label.pack(pady=10)

    # Close button
    close_btn = tk.Button(content, text="Zamknij",
                          command=instruction_window.destroy,
                          font=("Helvetica", 12),
                          bg=controller.button_color,
                          fg="white",
                          padx=10, pady=5)
    close_btn.pack(pady=15)
