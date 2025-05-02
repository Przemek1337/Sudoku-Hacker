import sys
import os
import torch
sys.path.append(os.path.abspath(".."))
from helper_methods import get_best_mask, get_corners, get_squares, correct_squares, plot_images, perspective_transform
from process import process_sudoku_image
from models import OurSmallModel, val_tfms
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
            return process_sudoku_image(image_path, self.model, self.val_tfms)

        except Exception as e:
            print(f"Error processing image: {str(e)}")
            raise