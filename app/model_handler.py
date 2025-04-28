import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
class ModelHandler:
    def __init__(self):
        self.model = None
        self.val_tfms = None

    def load_model(self):
        # self.model = load()
        # self.val_tfms = get_transforms()
        pass

    def process_image(self, image_path):
        try:
            if self.model is None:
                # test cases
                return np.array([
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]
                ])
            else:
                # (TODO) Connect our model and add logic to handle this else statement
                # return process_sudoku_image(image_path, self.model, self.val_tfms)
                pass
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            raise