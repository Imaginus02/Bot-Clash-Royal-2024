"""
Nom du fichier: ia_ingame_model.py
Auteur: Étienne-Théodore PRIN
Date: 2024-02-02

Description:
Ce module définie la classe VGG10 qui représente un CNN de type VGG10 pour classifier une image

Classe:
    - VGG10 : classe représentant un réseau neuronnal

Dépendances:
    - torch
"""

import torch.nn as nn

# Définition du modèle VGG-10
class VGG10(nn.Module):
    """
    Classe créant un réseau neuronnal de type CNN basé sur l'architecture du réseau VGG10

    Attributs:
        num_classes (int): nombre de classe différente des images (de base égale à 2)
    """
    def __init__(self, num_classes=2):
        super(VGG10, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.classifier = nn.Sequential(
            nn.Linear(256 * 7 * 7, 250),
            nn.ReLU(),
            nn.Dropout(),
            nn.Linear(250, 50),
            nn.ReLU(),
            nn.Dropout(),
            nn.Linear(50, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)  # Aplatir le tensor pour la classification
        x = self.classifier(x)
        return x
