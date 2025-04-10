import torchvision

from helper_methods import get_best_mask, get_corners, get_squares, correct_squares, plot_images
import os
from PIL import Image
# PyTorch
import torch
import cv2
import numpy as np
class DummyDataset:
    classes = [str(i) for i in range(1, 10)]

dataset = DummyDataset()
def process_sudoku_image(image_path, model, tfms):
    if not os.path.exists(image_path):
        print(f"Plik nie istnieje: {image_path}")
        return None, None
    colored_image = cv2.imread(image_path)
    if colored_image is None:
        print(f"Nie udało się wczytać obrazu: {image_path}")
        return None, None

    colored_image = cv2.cvtColor(colored_image, cv2.COLOR_BGR2RGB)
    image = cv2.cvtColor(colored_image, cv2.COLOR_BGR2GRAY)

    res_mask = get_best_mask(image.copy())
    corners = get_corners(res_mask)
    squares = get_squares(corners)

    numbers = correct_squares(image.copy(), squares)

    images = []
    labels = []
    predictions = np.zeros([9, 9], dtype=np.int32)

    model.eval()

    for index, number in enumerate(numbers):

        if number.sum() / 255 > np.prod(number.shape) / 60:

            pil_number = Image.fromarray(number)
            number = tfms(pil_number)
            x = number.unsqueeze(0)

            prediction = model(x)
            label = int(dataset.classes[torch.argmax(prediction, dim=1).item()])

            images.append(x[0][0].squeeze())
            labels.append(str(label))
            predictions[index//9, index%9] = label
        else:
            pil_number = Image.fromarray(number)
            number_tensor = tfms(pil_number)
            images.append(torch.zeros_like(number_tensor[0]))  # czarny kwadrat
    plot_images(numbers, 9, 9, labels=labels, figsize=(15,18))
    predictions_tensor = torch.tensor(predictions)
    print("\nPredykcje jako tensor PyTorch:")
    print(predictions_tensor)
    # predictions_tensor = torch.tensor(predictions)
    # print("\nPredykcje jako tensor PyTorch:")
    # print(predictions_tensor)
    # plt.figure(figsize=(15, 18))
    # for i in range(9 * 9):
    #     plt.subplot(9, 9, i + 1)
    #     plt.imshow(numbers[i], cmap='gray')
    #     plt.title(labels[i])
    #     plt.axis('off')
    # plt.tight_layout()
    # plt.show()
    return 0