import tkinter as tk

class ResultFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.background_color)
        self.controller = controller

        self.setup_layout()

    def setup_layout(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header_frame = tk.Frame(self, bg=self.controller.accent_color, padx=15, pady=10)
        header_frame.grid(row=0, column=0, sticky="ew")

        self.result_label = tk.Label(header_frame, text="Rozwiązanie Sudoku",
                                     font=("Helvetica", 16, "bold"),
                                     bg=self.controller.accent_color, fg="white")
        self.result_label.pack(side="left")

        content_frame = tk.Frame(self, bg=self.controller.background_color)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=0)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)

        grid_display_frame = tk.Frame(content_frame, bg="white", bd=2, relief="sunken")
        grid_display_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.sudoku_grid_frame = tk.Frame(grid_display_frame, bg="white")
        self.sudoku_grid_frame.pack(expand=True, fill="both", padx=10, pady=10)

        detected_grid_frame = tk.Frame(content_frame, bg="white", bd=2, relief="sunken")
        detected_grid_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.detected_grid_label = tk.Label(detected_grid_frame, text="Wykryta macierz Sudoku:",
                                            font=("Helvetica", 12, "bold"),
                                            bg="white")
        self.detected_grid_label.pack(pady=5)

        self.detected_grid_text = tk.Text(detected_grid_frame, height=15, width=30, font=("Courier", 12))
        self.detected_grid_text.pack(expand=True, fill="both", padx=10, pady=5)

        button_frame = tk.Frame(content_frame, bg=self.controller.background_color)
        button_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=15)

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

        back_to_input_btn = tk.Button(button_frame, text="Powrót do wczytywania",
                                      command=self.controller.show_sudoku,
                                      **button_style)
        back_to_input_btn.pack(side="left", padx=5)

        home_btn = tk.Button(button_frame, text="Powrót do menu",
                             command=self.controller.show_home,
                             **button_style)
        home_btn.pack(side="right", padx=5)

    def update_results(self, detected_grid, solution_grid):
        self.detected_grid_text.delete(1.0, tk.END)
        for row in detected_grid:
            row_str = ' '.join([str(num) if num != 0 else '.' for num in row])
            self.detected_grid_text.insert(tk.END, row_str + '\n')

        self.create_sudoku_grid_ui(solution_grid)

    def create_sudoku_grid_ui(self, grid_data):
        for widget in self.sudoku_grid_frame.winfo_children():
            widget.destroy()

        cell_size = 50
        for i in range(9):
            for j in range(9):
                bg_color = "white"
                if (i // 3 + j // 3) % 2 == 0:
                    bg_color = self.controller.grid_color

                cell_frame = tk.Frame(self.sudoku_grid_frame, width=cell_size, height=cell_size,
                                      bg=bg_color, highlightbackground=self.controller.border_color,
                                      highlightthickness=1)
                cell_frame.grid(row=i, column=j)
                cell_frame.grid_propagate(False)

                value = grid_data[i][j]
                if value != 0:
                    label = tk.Label(cell_frame, text=str(value), font=("Helvetica", 16, "bold"),
                                     bg=bg_color)
                    label.place(relx=0.5, rely=0.5, anchor="center")

        for i in range(3):
            for j in range(3):
                border_frame = tk.Frame(self.sudoku_grid_frame, bg=self.controller.border_color,
                                        width=(3 * cell_size + 2), height=(3 * cell_size + 2))
                border_frame.place(x=j * 3 * cell_size - 1, y=i * 3 * cell_size - 1)
                border_frame.lower()