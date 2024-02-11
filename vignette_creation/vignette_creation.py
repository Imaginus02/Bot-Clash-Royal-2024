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

image_path = '11.png'
new_image_name= 'tower.jpg'

image = cv2.imread(image_path)

if image is not None:

    x=78
    y=456
    w=54
    h=65

    roi = image[y:y+h, x:x+w]

    plt.imshow(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
    # Enregistre la région découpée
    cv2.imwrite(new_image_name, roi)
    plt.show()
else:
    print("Erreur : impossible de charger l'image")
