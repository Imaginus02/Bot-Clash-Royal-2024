"""
Nom du fichier: train_yolo.py
Auteur: Étienne-Théodore PRIN
Date: 2024-02-02

Description:
Ce module effectue l'entrainement d'un yolo v8 pour labeliser des images

Dépendances:
    -ultralytics
"""

from ultralytics import YOLO


if __name__ == '__main__':
    # Load a model
    model = YOLO('yolov8m.pt')  # load a pretrained model

    # Train the model
    results = model.train(data='clash_labelled3\data.yaml', epochs=300, imgsz=800)