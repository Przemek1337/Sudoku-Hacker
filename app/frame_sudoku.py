import tkinter as tk
from PIL import Image, ImageTk
import cv2


class SudokuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.background_color)
        self.controller = controller

        self.original_cv_image = None
        self.canvas_image = None

        self.setup_layout()

    def setup_layout(self):
        # Configure layout
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header frame
        header_frame = tk.Frame(self, bg=self.controller.accent_color, padx=15, pady=10)
        header_frame.grid(row=0, column=0, sticky="ew")

        self.label = tk.Label(header_frame, text="Wczytaj zdjęcie Sudoku",
                              font=("Helvetica", 16, "bold"),
                              bg=self.controller.accent_color, fg="white")
        self.label.pack(side="left")

        # Content frame
        content_frame = tk.Frame(self, bg=self.controller.background_color)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=0)
        content_frame.grid_columnconfigure(0, weight=1)

        # Canvas frame
        canvas_frame = tk.Frame(content_frame, bg="white", bd=2, relief="sunken",
                                highlightbackground=self.controller.border_color)
        canvas_frame.grid(row=0, column=0, sticky="nsew", pady=10)

        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(canvas_frame, bg="gray")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Button frame
        button_frame = tk.Frame(content_frame, bg=self.controller.background_color)
        button_frame.grid(row=1, column=0, sticky="ew", pady=15)

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

        # Button style
        button_style = {
            "font": ("Helvetica", 12),
            "bg": self.controller.button_color,
            "fg": "white",
            "activebackground": self.controller.grid_color,
            "relief": "raised",
            "bd": 2,
            "padx": 10,
            "pady": 5
        }

        # Buttons
        self.load_btn = tk.Button(button_frame, text="Wczytaj obraz",
                                  command=self.controller.load_image, **button_style)
        self.load_btn.grid(row=0, column=0, padx=5)

        self.solve_btn = tk.Button(button_frame, text="Rozwiąż Sudoku",
                                   command=self.controller.solve_sudoku, **button_style)
        self.solve_btn.grid(row=0, column=1, padx=5)

        back_btn = tk.Button(button_frame, text="Powrót do menu",
                             command=self.controller.show_home,
                             font=("Helvetica", 10),
                             bg=self.controller.background_color,
                             fg=self.controller.text_color)
        back_btn.grid(row=0, column=2, padx=5)

    def set_image(self, cv_image):
        self.original_cv_image = cv_image
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

    def set_processing_status(self, is_processing):
        if is_processing:
            self.label.config(text="AI w trakcie rozwiązywania Sudoku...")
            self.solve_btn.config(state=tk.DISABLED)
            self.load_btn.config(state=tk.DISABLED)
        else:
            self.label.config(text="Wczytaj zdjęcie Sudoku")
            self.solve_btn.config(state=tk.NORMAL)
            self.load_btn.config(state=tk.NORMAL)
