import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2


class SudokuSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Sudoku Solver")
        self.root.geometry("800x700")


        self.background_color = "#c2b280"  # Jasny beżowy/brązowy
        self.accent_color = "#8B4513"  # Brązowy
        self.button_color = "#A0522D"  # Ciemniejszy brąz
        self.text_color = "#3A1F04"  # Ciemny brąz
        self.grid_color = "#D2B48C"  # Jasny brąz
        self.border_color = "#654321"  # Ciemny brąz dla obramowań

        # Ustawienie tła aplikacji
        self.root.configure(bg=self.background_color)


        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)


        self.home_frame = tk.Frame(root, bg=self.background_color)
        self.sudoku_frame = tk.Frame(root, bg=self.background_color)


        for frame in [self.home_frame, self.sudoku_frame]:
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)


        self.setup_home_frame()
        self.setup_sudoku_frame()


        self.show_home()


        self.root.bind("<Configure>", self.on_window_resize)

    def on_window_resize(self, event):

        if event.widget == self.root:
            self.update_layout()

    def update_layout(self):

        if hasattr(self, 'canvas') and hasattr(self, 'original_cv_image') and self.original_cv_image is not None:
            self.resize_canvas_image()

    def setup_home_frame(self):

        self.home_frame.grid_rowconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(0, weight=1)

        content_frame = tk.Frame(self.home_frame, bg=self.background_color)
        content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        content_frame.grid_rowconfigure(0, weight=0)
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_rowconfigure(2, weight=0)
        content_frame.grid_columnconfigure(0, weight=1)


        title_frame = tk.Frame(content_frame, bg=self.accent_color, padx=20, pady=15, relief="raised", bd=2)
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        title_label = tk.Label(title_frame, text="AI SUDOKU SOLVER",
                               font=("Helvetica", 24, "bold"),
                               bg=self.accent_color, fg="white")
        title_label.pack()

        subtitle_label = tk.Label(title_frame, text="Rozwiązywanie Sudoku przy pomocy sztucznej inteligencji",
                                  font=("Helvetica", 12),
                                  bg=self.accent_color, fg="white")
        subtitle_label.pack(pady=5)


        button_container = tk.Frame(content_frame, bg=self.background_color)
        button_container.grid(row=1, column=0)

        button_frame = tk.Frame(button_container, bg=self.background_color)
        button_frame.pack(expand=True)


        button_style = {
            "font": ("Helvetica", 14),
            "width": 18,
            "height": 2,
            "bg": self.button_color,
            "fg": "white",
            "activebackground": self.grid_color,
            "activeforeground": self.text_color,
            "relief": "raised",
            "bd": 2
        }


        start_btn = tk.Button(button_frame, text="Rozpocznij", command=self.show_sudoku, **button_style)
        start_btn.pack(pady=15)

        instruction_btn = tk.Button(button_frame, text="Instrukcja obsługi", command=self.show_instructions,
                                    **button_style)
        instruction_btn.pack(pady=15)

        about_btn = tk.Button(button_frame, text="O aplikacji", command=self.show_about, **button_style)
        about_btn.pack(pady=15)


        footer = tk.Label(content_frame, text="© 2025 AI Sudoku Solver",
                          font=("Helvetica", 8),
                          bg=self.background_color, fg=self.text_color)
        footer.grid(row=2, column=0, sticky="s", pady=10)

    def setup_sudoku_frame(self):

        self.sudoku_frame.grid_rowconfigure(0, weight=0)
        self.sudoku_frame.grid_rowconfigure(1, weight=1)
        self.sudoku_frame.grid_columnconfigure(0, weight=1)


        header_frame = tk.Frame(self.sudoku_frame, bg=self.accent_color, padx=15, pady=10)
        header_frame.grid(row=0, column=0, sticky="ew")

        self.label = tk.Label(header_frame, text="Wczytaj zdjęcie Sudoku",
                              font=("Helvetica", 16, "bold"),
                              bg=self.accent_color, fg="white")
        self.label.pack(side="left")


        content_frame = tk.Frame(self.sudoku_frame, bg=self.background_color)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=0)
        content_frame.grid_columnconfigure(0, weight=1)


        canvas_frame = tk.Frame(content_frame, bg="white", bd=2, relief="sunken", highlightbackground=self.border_color)
        canvas_frame.grid(row=0, column=0, sticky="nsew", pady=10)

        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(canvas_frame, bg="gray")
        self.canvas.grid(row=0, column=0, sticky="nsew")


        self.canvas.bind("<Configure>", self.resize_canvas_event)


        button_frame = tk.Frame(content_frame, bg=self.background_color)
        button_frame.grid(row=1, column=0, sticky="ew", pady=15)


        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)


        button_style = {
            "font": ("Helvetica", 12),
            "bg": self.button_color,
            "fg": "white",
            "activebackground": self.grid_color,
            "relief": "raised",
            "bd": 2,
            "padx": 10,
            "pady": 5
        }


        self.load_btn = tk.Button(button_frame, text="Wczytaj obraz", command=self.load_image, **button_style)
        self.load_btn.grid(row=0, column=0, padx=5)

        self.solve_btn = tk.Button(button_frame, text="Rozwiąż Sudoku", command=self.solve_sudoku, **button_style)
        self.solve_btn.grid(row=0, column=1, padx=5)


        back_btn = tk.Button(button_frame, text="Powrót do menu",
                             command=self.show_home,
                             font=("Helvetica", 10),
                             bg=self.background_color,
                             fg=self.text_color)
        back_btn.grid(row=0, column=2, padx=5)

        self.image = None
        self.original_cv_image = None

    def resize_canvas_event(self, event):

        self.resize_canvas_image()

    def resize_canvas_image(self):
        if self.original_cv_image is None:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1 or canvas_height <= 1:
            return

        resized_cv_image = cv2.resize(self.original_cv_image, (canvas_width, canvas_height))
        image_pil = Image.fromarray(resized_cv_image)
        self.canvas_image = ImageTk.PhotoImage(image_pil)

        self.canvas.delete("all")
        self.canvas.create_image(canvas_width / 2, canvas_height / 2, image=self.canvas_image, anchor=tk.CENTER)
        self.canvas.image = self.canvas_image

    def show_home(self):

        self.sudoku_frame.grid_remove()
        self.home_frame.grid(row=0, column=0, sticky="nsew")

    def show_sudoku(self):

        self.home_frame.grid_remove()
        self.sudoku_frame.grid(row=0, column=0, sticky="nsew")

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Obrazy", "*.jpg *.png")])
        if not file_path:
            return

        # Wczytanie obrazu
        self.original_cv_image = cv2.imread(file_path)
        self.original_cv_image = cv2.cvtColor(self.original_cv_image, cv2.COLOR_BGR2RGB)


        self.root.after(100, self.resize_canvas_image)

    def solve_sudoku(self):
        # TU model AI
        self.label.config(text="AI w trakcie rozwiązywania Sudoku...")
        messagebox.showinfo("Rozwiązywanie", "Rozpoczęto analizę obrazu i rozwiązywanie Sudoku...")

    def show_instructions(self):
        instruction_window = tk.Toplevel(self.root)
        instruction_window.title("Instrukcja obsługi")
        instruction_window.geometry("600x400")
        instruction_window.configure(bg=self.background_color)


        header = tk.Frame(instruction_window, bg=self.accent_color, padx=15, pady=10)
        header.pack(fill="x")

        title = tk.Label(header, text="Instrukcja obsługi programu",
                         font=("Helvetica", 16, "bold"),
                         bg=self.accent_color, fg="white")
        title.pack()


        content = tk.Frame(instruction_window, bg=self.background_color, padx=20, pady=20)
        content.pack(fill="both", expand=True)

        instructions_text = """
        Jak korzystać z aplikacji Sudoku Solver:

        1. Na stronie głównej kliknij przycisk "Rozpocznij".

        2. Na ekranie rozwiązywania Sudoku kliknij "Wczytaj obraz" i wybierz 
           zdjęcie planszy Sudoku z Twojego komputera.

        3. Po wczytaniu obrazu kliknij "Rozwiąż Sudoku".

        4. Program   rozpoznana plansze 
           i rozwiązaniązę sudoku.
        """

        instruction_label = tk.Label(content, text=instructions_text,
                                     font=("Helvetica", 11),
                                     bg=self.background_color, fg=self.text_color,
                                     justify="left")
        instruction_label.pack(pady=10)


        close_btn = tk.Button(content, text="Zamknij",
                              command=instruction_window.destroy,
                              font=("Helvetica", 12),
                              bg=self.button_color,
                              fg="white",
                              padx=10, pady=5)
        close_btn.pack(pady=15)

    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("O aplikacji")
        about_window.geometry("600x400")
        about_window.configure(bg=self.background_color)


        header = tk.Frame(about_window, bg=self.accent_color, padx=15, pady=10)
        header.pack(fill="x")

        title = tk.Label(header, text="O aplikacji AI Sudoku Solver",
                         font=("Helvetica", 16, "bold"),
                         bg=self.accent_color, fg="white")
        title.pack()


        content = tk.Frame(about_window, bg=self.background_color, padx=20, pady=20)
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
                               bg=self.background_color, fg=self.text_color,
                               justify="left")
        about_label.pack(pady=10)


        close_btn = tk.Button(content, text="Zamknij",
                              command=about_window.destroy,
                              font=("Helvetica", 12),
                              bg=self.button_color,
                              fg="white",
                              padx=10, pady=5)
        close_btn.pack(pady=15)



if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverApp(root)
    root.mainloop()