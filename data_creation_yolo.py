"""
Nom du fichier: data_creation_yolo.py
Auteur: Étienne-Théodore PRIN
Date: 2024-02-02

Description:
Ce module fait le lien entre différentes classes du projet Bot clash Royal pour sauvegarder 
    toutes les secondes une images du jeu pour créer une base de donnée d'image de jeu principalement pour le yolo.
On peut choisir de sauvegarder uniquement les images en jeu ou en menu à l'aide de la ligne 39

Dépendances:
    - open cv (cv2)
    - time
    - nécessite la création du CNN vgg10 (initialisable avec ai_creation.ia_ingame.ia_ingame_learning.py) 
    - classes trouvable dans le dossier use_fonction
"""

import time
import cv2

from use_fonction.screen_capture.capture_windows import Screen_video_capture
from use_fonction.screen_analyse import Screen_analyse

# Créer système de capture video
windows_capture = Screen_video_capture()

# créer l'analyseur d'image
analyse = Screen_analyse()

running = True
i=0
old_state=True
while running:
    image = windows_capture.get_screen()
    state = analyse.get_state(image)
    if state[0]!=old_state:
        old_state=state[0]
        print(state[0])
    if state[0]==True: #False pour enregistrer des images du menu et True pour enregistrer les images en partie
        image_bgr_final = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # cv2.imwrite('io_game/in_game/'+str(i)+'.png', image_bgr_final)
        cv2.imwrite('image_non_labelise/'+str(i)+'.png', image_bgr_final)
        i+=1
    time.sleep(1)