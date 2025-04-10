import torch
import numpy as np
#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#print(f"Używane urządzenie: {device}")
from torchmetrics.functional import accuracy
# PyTorch
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader, random_split
import torchvision
from PIL import Image
# PyTorch Lightning
import pytorch_lightning as pl
#from pytorch_lightning.metrics.functional import accuracy

import cv2
import numpy as np
from skimage import feature
import matplotlib.pyplot as plt

torch.manual_seed(0)

tfms = torchvision.transforms.Compose([
  torchvision.transforms.RandomRotation(10.0),
  torchvision.transforms.RandomResizedCrop([28, 28], (0.9, 1.0)),
  torchvision.transforms.ToTensor(),
  torchvision.transforms.Normalize((0.1307,), (0.3081,))
])

val_tfms = torchvision.transforms.Compose([
  torchvision.transforms.ToTensor(),
  torchvision.transforms.Normalize((0.1307,), (0.3081,))
])

dataset = torchvision.datasets.ImageFolder("/home/przemekk/PycharmProjects/pl_sudoku/Sudoku-Solver/datasets", loader=Image.open, transform=tfms)

print(f"Total length of dataset: {len(dataset)}")
train_size = int(len(dataset) * 0.9)
valid_size = len(dataset) - train_size

dataset_train, dataset_val = random_split(dataset, [train_size, valid_size])
print(f"Total length of train dataset: {len(dataset_train)}")
print(f"Total length of valid dataset: {len(dataset_val)}")

class OurSmallModel(pl.LightningModule):

    def __init__(self, learning_rate=0.0003):
      super().__init__()

      self.learning_rate = learning_rate

      self.layer1 = nn.Linear(28*28, 2000)
      self.layer2 = nn.Linear(2000, 500)
      self.output_layer = nn.Linear(500, 10)

    def forward(self, x):
      # Zamiana 2-wymiarowego zdjęcia na 1-wymiarowe (tak jakby)
      # Oryginalnie [16, 28, 28]
      # Finalnie [16, 28*28]
      x = x.view(x.shape[0], 28*28)

      x = self.layer1(x)
      x = F.relu(x)

      x = self.layer2(x)
      x = F.relu(x)

      x = self.output_layer(x)

      return F.log_softmax(x, dim=1)


    # to funkcja która wykona się przy każdym kroku w treningu
    def training_step(self, batch, batch_idx):
      # x: co wkładamy do modelu
      # y: odpowiedź której od modelu oczekujemy
      x, y = batch

      # przepuszczenie danych przez model
      prediction = self(x)

      # obliczenie lossa
      loss = F.mse_loss(prediction, F.one_hot(y, num_classes=10).float())
      return loss

    # to funkcja która wykona się przy każdym kroku w walidacji
    def validation_step(self, batch, batch_idx):
      x, y = batch

      # przepuszczenie danych przez model
      prediction = self(x)

      # obliczenie lossa
      loss = F.mse_loss(prediction, F.one_hot(y, num_classes=10).float())

      predicted_number = torch.argmax(prediction, dim=1)
      # policzenie "celności" modelu
      prediction_accuracy = accuracy(prediction, y, task="multiclass", num_classes=10)

      # wypisanie naszych statystyk walidacyjnych
      self.log('val_loss', loss, prog_bar=True)
      self.log('val_acc', prediction_accuracy, prog_bar=True)

      return loss

    # W tej fukcji definiujemy sobie optimizer
    def configure_optimizers(self):
      optimizer = torch.optim.Adam(model.parameters(), lr=self.learning_rate)
      return optimizer

    # W tej funkcji definiujemy dataloader do treningu
    def train_dataloader(self):
      return DataLoader(dataset_train, batch_size=16, num_workers=8)

    # W tej funkcji definiujemy dataloader do walidacji
    def val_dataloader(self):
      return DataLoader(dataset_val, batch_size=16, num_workers=8)