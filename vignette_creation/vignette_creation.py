"""
Nom du fichier: vignette_creation.py
Auteur: Étienne-Théodore PRIN
Date: 2024-02-02

Description:
Ce module creer et enregistre une vignette d'une image.
La vignette correspond à la partie indiqué par x,y,w,h

Dépendances:
    - open CV (cv2)
    - matplolib
"""

import cv2
from matplotlib import pyplot as plt

image_path = 'D:\\clash royale\\Bot-Clash-Royal-2023\\image_non_labelise\\23.png'
new_image_name= 'gobelin_vignette.jpg'

image = cv2.imread(image_path)

if image is not None:

    x=140
    y=23
    w=73
    h=92

    roi = image[y:y+h, x:x+w]

    plt.imshow(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
    # Enregistre la région découpée
    cv2.imwrite(new_image_name, roi)
    plt.show()
else:
    print("Erreur : impossible de charger l'image")
