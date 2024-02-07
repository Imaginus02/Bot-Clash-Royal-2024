"""
Nom du fichier: data_creation_VGG.py
Auteur: Étienne-Théodore PRIN
Date: 2024-02-02

Description:
Ce module fait le lien entre différentes classes du projet Bot clash Royal pour sauvegarder 
    toutes les secondes une images du jeu pour créer une base de donnée d'image principalement pour le réseau VGG.

Dépendances:
    - open cv (cv2)
    - time
    - classes trouvable dans le dossier use_fonction
"""

import time
import cv2

from use_fonction.screen_capture.capture_windows import Screen_video_capture

# Créer système de capture video
windows_capture = Screen_video_capture()

running = True
i=0
while running:
    image = windows_capture.get_screen()
    image_bgr_final = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # cv2.imwrite('io_game/in_game/'+str(i)+'.png', image_bgr_final)
    cv2.imwrite('image_non_labelise/'+str(i)+'.png', image_bgr_final)
    i+=1
    time.sleep(1)