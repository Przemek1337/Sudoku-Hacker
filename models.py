from torchmetrics.functional import accuracy
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader, random_split
import torchvision
from PIL import Image
import pytorch_lightning as pl
import os
from pytorch_lightning.callbacks import Callback
import matplotlib.pyplot as plt
from torch.utils.data import Subset
from collections import Counter
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "datasets", "preprocessed")
dataset_base = torchvision.datasets.ImageFolder(DATASET_DIR, loader=Image.open)

train_size = int(len(dataset_base) * 0.9)
valid_size = len(dataset_base) - train_size
train_indices, val_indices = torch.utils.data.random_split(range(len(dataset_base)), [train_size, valid_size])

print(f"Total length of dataset: {len(dataset_base)}")
print(f"Train size: {len(train_indices)}")
print(f"Validation size: {len(val_indices)}")
dataset_base = torchvision.datasets.ImageFolder(DATASET_DIR, loader=Image.open)
print("Podfoldery (klasy):", dataset_base.classes)

print("Rozkład etykiet:", Counter([label for _, label in dataset_base]))
dataset_train = Subset(
    torchvision.datasets.ImageFolder(DATASET_DIR, loader=Image.open, transform=tfms),
    train_indices
)

dataset_val = Subset(
    torchvision.datasets.ImageFolder(DATASET_DIR, loader=Image.open, transform=val_tfms),
    val_indices
)

print(f"Train size: {len(dataset_train)}")
print(f"Validation size: {len(dataset_val)}")


class MetricsCallback(Callback):
  def __init__(self):
    self.train_losses = []
    self.val_losses = []
    self.val_accuracies = []
    self.epoch = []

  def on_train_epoch_end(self, trainer, pl_module):
    if trainer.logged_metrics:
      epoch = trainer.current_epoch
      self.epoch.append(epoch)

      if 'val_loss' in trainer.logged_metrics:
        self.val_losses.append(trainer.logged_metrics['val_loss'].item())
      if 'val_acc' in trainer.logged_metrics:
        self.val_accuracies.append(trainer.logged_metrics['val_acc'].item())

class OurSmallModel(pl.LightningModule):

    def __init__(self, learning_rate=0.0003, model_name="Modelv1"):
      super().__init__()

      self.learning_rate = learning_rate
      self.model_name = model_name

      self.train_losses = []
      self.val_losses = []
      self.val_accuracies = []
      self.train_accuracies = []

      self.layer1 = nn.Linear(28*28, 2048)
      self.layer2 = nn.Linear(2048, 512)
      self.output_layer = nn.Linear(512, 9)

    def forward(self, x):
      x = x.view(x.shape[0], 28*28)
      x = self.layer1(x)
      x = F.relu(x)

      x = self.layer2(x)
      x = F.relu(x)
      x = self.output_layer(x)

      return F.log_softmax(x, dim=1)


    def training_step(self, batch, batch_idx):
      x, y = batch
      prediction = self(x)

      loss = F.nll_loss(prediction, y)
      acc = accuracy(prediction, y, task='multiclass', num_classes=9)
      self.log('train_loss', loss, prog_bar=True)
      self.log('train_acc', acc, prog_bar=True)
      return loss

    def validation_step(self, batch, batch_idx):
      x, y = batch
      prediction = self(x)

      loss = F.nll_loss(prediction, y)
      acc = accuracy(prediction, y, task='multiclass', num_classes=9)

      self.log('val_loss', loss, on_step=False, on_epoch=True, prog_bar=True)
      self.log('val_acc', acc, on_step=False, on_epoch=True, prog_bar=True)

      return loss

    def on_train_epoch_end(self):
      if 'train_loss' in self.trainer.logged_metrics:
        self.train_losses.append(self.trainer.logged_metrics['train_loss'].item())
      if 'train_acc' in self.trainer.logged_metrics:
        self.train_accuracies.append(self.trainer.logged_metrics['train_acc'].item())

    def on_validation_epoch_end(self):
      if 'val_loss' in self.trainer.logged_metrics:
        self.val_losses.append(self.trainer.logged_metrics['val_loss'].item())
      if 'val_acc' in self.trainer.logged_metrics:
        self.val_accuracies.append(self.trainer.logged_metrics['val_acc'].item())

    def configure_optimizers(self):
      optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate)
      return optimizer

    def train_dataloader(self):
      return DataLoader(dataset_train, batch_size=16, num_workers=8)

    def val_dataloader(self):
      return DataLoader(dataset_val, batch_size=16, num_workers=8)

    def plot_metrics(self, save_path=None):
      if not self.val_losses or not self.val_accuracies:
        print("Brak metryk do wyplotowania. Czy model był trenowany?")
        return

      fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

      epochs = range(1, len(self.val_losses) + 1)

      if self.train_losses and len(self.train_losses) == len(self.val_losses):
        ax1.plot(epochs, self.train_losses, 'b-', label='Training Loss', linewidth=2)
      ax1.plot(epochs, self.val_losses, 'r-', label='Validation Loss', linewidth=2)
      ax1.set_title(f'{self.model_name} - Loss')
      ax1.set_xlabel('Epoka')
      ax1.set_ylabel('Loss')
      ax1.legend()
      ax1.grid(True, alpha=0.3)

      ax2.plot(epochs, self.val_accuracies, 'g-', label='Validation Accuracy', linewidth=2)
      ax2.set_title(f'{self.model_name} - Accuracy')
      ax2.set_xlabel('Epoka')
      ax2.set_ylabel('Accuracy')
      ax2.legend()
      ax2.grid(True, alpha=0.3)
      ax2.set_ylim(0, 1)

      plt.tight_layout()

      if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Wykres zapisany do: {save_path}")

      plt.show()

      if self.val_accuracies and self.val_losses:
        final_acc = self.val_accuracies[-1]
        best_acc = max(self.val_accuracies)
        final_loss = self.val_losses[-1]

        print(f"\n=== STATYSTYKI {self.model_name} ===")
        print(f"Końcowa accuracy: {final_acc:.4f}")
        print(f"Najlepsza accuracy: {best_acc:.4f}")
        print(f"Końcowy loss: {final_loss:.4f}")
        print(f"Liczba epok: {len(self.val_accuracies)}")