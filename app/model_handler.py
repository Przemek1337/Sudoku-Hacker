import numpy as np
import sys
import os
import torch
import torchvision
sys.path.append(os.path.abspath(".."))
from helper_methods import get_best_mask, get_corners, get_squares, correct_squares, plot_images, perspective_transform
from process import process_sudoku_image
from models import OurSmallModel, val_tfms
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

sys.modules['__main__'].OurSmallModel = OurSmallModel
class ModelHandler:
    def __init__(self):
        try:
            self.model = torch.load("/home/przemek/PycharmProjects/AI_projec/Sudoku-Hacker/notebooks/model.pt",
                                    weights_only=False)
            self.val_tfms = val_tfms

        except Exception as ex:
            print(f"Failed to load model {ex}")
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
                return process_sudoku_image(image_path, self.model, self.val_tfms)

        except Exception as e:
            print(f"Error processing image: {str(e)}")
            raise