import tkinter as tk


class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.background_color)
        self.controller = controller

        self.setup_layout()

    def setup_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content_frame = tk.Frame(self, bg=self.controller.background_color)
        content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        content_frame.grid_rowconfigure(0, weight=0)
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_rowconfigure(2, weight=0)
        content_frame.grid_columnconfigure(0, weight=1)

        title_frame = tk.Frame(content_frame, bg=self.controller.accent_color, padx=20, pady=15, relief="raised", bd=2)
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        title_label = tk.Label(title_frame, text="AI SUDOKU SOLVER",
                               font=("Helvetica", 24, "bold"),
                               bg=self.controller.accent_color, fg="white")
        title_label.pack()

        subtitle_label = tk.Label(title_frame, text="Rozwiązywanie Sudoku przy pomocy sztucznej inteligencji",
                                  font=("Helvetica", 12),
                                  bg=self.controller.accent_color, fg="white")
        subtitle_label.pack(pady=5)

        button_container = tk.Frame(content_frame, bg=self.controller.background_color)
        button_container.grid(row=1, column=0)

        button_frame = tk.Frame(button_container, bg=self.controller.background_color)
        button_frame.pack(expand=True)

        # Button style
        button_style = {
            "font": ("Helvetica", 14),
            "width": 18,
            "height": 2,
            "bg": self.controller.button_color,
            "fg": "white",
            "activebackground": self.controller.grid_color,
            "activeforeground": self.controller.text_color,
            "relief": "raised",
            "bd": 2
        }

        start_btn = tk.Button(button_frame, text="Rozpocznij", command=self.controller.show_sudoku, **button_style)
        start_btn.pack(pady=15)

        instruction_btn = tk.Button(button_frame, text="Instrukcja obsługi",
                                    command=self.controller.show_instructions, **button_style)
        instruction_btn.pack(pady=15)

        about_btn = tk.Button(button_frame, text="O aplikacji",
                              command=self.controller.show_about, **button_style)
        about_btn.pack(pady=15)

        footer = tk.Label(content_frame, text="© 2025 AI Sudoku Solver",
                          font=("Helvetica", 8),
                          bg=self.controller.background_color, fg=self.controller.text_color)
        footer.grid(row=2, column=0, sticky="s", pady=10)
