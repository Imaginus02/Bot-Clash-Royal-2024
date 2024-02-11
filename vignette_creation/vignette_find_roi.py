"""
Nom du fichier: vignette_find_roi.py
Auteur: Étienne-Théodore PRIN
Date: 2024-02-02

Description:
Ce module trouve les dimensions de la bounding boxe correspondant à la 
position de la vignette dans l'image modèle

Dépendances:
    - open CV (cv2)
    - matplolib
"""

import cv2
from matplotlib import pyplot as plt

# Charger l'image cible et l'image modèle (ROI)
image_cible = cv2.imread('11.png')
image_modele = cv2.imread('tower.jpg')  # La ROI/vignette

x=78
y=456
w=54
h=65

image_cible=image_cible[:, :]

# Correspondance de modèles
resultat = cv2.matchTemplate(image_cible, image_modele, cv2.TM_CCOEFF_NORMED)

# Trouver la position de la meilleure correspondance
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultat)

print("Correspondance : ",max_val)

# Coordonnées du coin supérieur gauche de la meilleure correspondance
x, y = max_loc

# Dimensions de la ROI
h, w = image_modele.shape[:2]

print("ROI : ",[x,y,w,h])

# Dessiner un rectangle autour de la zone correspondante
cv2.rectangle(image_cible, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Afficher l'image avec le rectangle
plt.imshow(cv2.cvtColor(image_cible, cv2.COLOR_BGR2RGB))
plt.title('Correspondance trouvée')
plt.show()