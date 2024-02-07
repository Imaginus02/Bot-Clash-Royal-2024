"""
Nom du fichier: ia_ingame_learning.py
Auteur: Étienne-Théodore PRIN
Date: 2024-02-02

Description:
Ce module effectue l'entrainement d'un CNN de type VGG10 pour classifié des images entre deux classes

Dépendances:
    - Nécessite la présence d'une base de donnée dans le dossier io_ingame
    - torch
    - torchvision
    - ia_ingame_model.py 
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split
from ia_ingame_model import VGG10

# Choix du moteur de calcul (CPU ou GPU)
cuda_available = torch.cuda.is_available()
print("CUDA disponible:", cuda_available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Paramètres
learning_rate = 0.001
batch_size = 32
epochs = 10
num_classes = 2  # Adaptez en fonction du nombre de classes différentes

# Transformations des données
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Chargement de l'ensemble de données
dataset = datasets.ImageFolder(root='../../io_game', transform=transform)

# Tailles pour la division en ensembles d'entraînement, de validation et de test
train_size = int(0.80 * len(dataset))
val_size = int(0.20 * len(dataset))
test_size = len(dataset) - train_size - val_size
print(train_size)
# Division des données
train_dataset, val_dataset, test_dataset = random_split(dataset, [train_size, val_size, test_size])

# Création des chargeurs de données
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=True)

# Initialisation du modèle
model = VGG10(num_classes=num_classes).to(device)

# Critère de perte et optimiseur
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Entraînement du modèle
for epoch in range(epochs):
    model.train()
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()

        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

    # Validation
    model.eval()
    total = 0
    correct = 0
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    # Calculer la précision totale
    accuracy = 100 * correct / total
    print(f'Epoch {epoch+1}/{epochs}, Train Loss: {loss.item():.4f}, Validation Accuracy: {100 * correct / total:.2f}%')

# Sauvegarde du modèle
torch.save(model.state_dict(), 'vgg10_model.pth')
