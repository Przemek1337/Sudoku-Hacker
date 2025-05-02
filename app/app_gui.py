from tkinter import filedialog, messagebox
import cv2
import threading
from frame_home import HomeFrame
from frame_sudoku import SudokuFrame
from frame_result import ResultFrame
from dialog_instructions import show_instructions_dialog
from dialog_about import show_about_dialog

class SudokuSolverApp:
    def __init__(self, root, model_handler, solver):
        self.root = root
        self.root.title("AI Sudoku Hacker")
        self.root.geometry("800x700")

        self.model_handler = model_handler
        self.solver = solver

        self.setup_colors()

        self.root.configure(bg=self.background_color)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.create_frames()

        self.image = None
        self.original_cv_image = None
        self.detected_grid = None
        self.solution_grid = None
        self.image_path = None

        self.show_home()

        self.root.bind("<Configure>", self.on_window_resize)

    def setup_colors(self):
        self.background_color = "#c2b280"  # Jasny beżowy/brązowy
        self.accent_color = "#8B4513"  # Brązowy
        self.button_color = "#A0522D"  # Ciemniejszy brąz
        self.text_color = "#3A1F04"  # Ciemny brąz
        self.grid_color = "#D2B48C"  # Jasny brąz
        self.border_color = "#654321"  # Ciemny brąz dla obramowań

    def create_frames(self):
        self.home_frame = HomeFrame(self.root, self)
        self.sudoku_frame = SudokuFrame(self.root, self)
        self.result_frame = ResultFrame(self.root, self)

        for frame in [self.home_frame, self.sudoku_frame, self.result_frame]:
            frame.grid(row=0, column=0, sticky="nsew")

    def on_window_resize(self, event):
        if event.widget == self.root:
            self.update_layout()

    def update_layout(self):
        self.sudoku_frame.resize_canvas_image()

    def show_home(self):
        self.sudoku_frame.grid_remove()
        self.result_frame.grid_remove()
        self.home_frame.grid()

    def show_sudoku(self):
        self.home_frame.grid_remove()
        self.result_frame.grid_remove()
        self.sudoku_frame.grid()

    def show_result(self):
        self.home_frame.grid_remove()
        self.sudoku_frame.grid_remove()
        self.result_frame.grid()

    def load_image(self, file_path=None):
        if file_path is None:
            file_path = filedialog.askopenfilename(filetypes=[("Obrazy", "*.jpg *.png")])
            if not file_path:
                return

        self.original_cv_image = cv2.imread(file_path)
        self.original_cv_image = cv2.cvtColor(self.original_cv_image, cv2.COLOR_BGR2RGB)
        self.image_path = file_path

        self.sudoku_frame.set_image(self.original_cv_image)

    def solve_sudoku(self):
        if self.original_cv_image is None and not hasattr(self, 'image_path'):
            messagebox.showinfo("Informacja", "Najpierw wczytaj obraz Sudoku.")
            return

        self.sudoku_frame.set_processing_status(True)
        messagebox.showinfo("Rozwiązywanie", "Rozpoczęto analizę obrazu i rozwiązywanie Sudoku, kliknij 'ok'")

        def process_thread():
            try:
                self.detected_grid = self.model_handler.process_image(self.image_path)

                if self.detected_grid is not None:

                    self.solution_grid = self.solver.solve(self.detected_grid)

                    self.root.after(0, self.show_results)
                else:
                    self.root.after(0, lambda: messagebox.showerror("Błąd",
                                                                    "Nie udało się wykryć planszy Sudoku na obrazie."))
                    self.sudoku_frame.set_processing_status(False)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Błąd", f"Wystąpił błąd: {str(e)}"))
                self.sudoku_frame.set_processing_status(False)

        threading.Thread(target=process_thread).start()

    def show_results(self):
        self.result_frame.update_results(self.detected_grid, self.solution_grid)

        self.show_result()

        self.sudoku_frame.set_processing_status(False)

    def show_instructions(self):
        show_instructions_dialog(self.root, self)

    def show_about(self):
        show_about_dialog(self.root, self)