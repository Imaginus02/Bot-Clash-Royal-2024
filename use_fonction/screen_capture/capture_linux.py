"""
Nom du fichier: capture_linux.py
Auteur: Étienne-Théodore PRIN
Date: 2024-02-02

Description:
Ce module est utilisé uniquement si l'os de l'ordinateur est linux
Ce module définie la classe Screen_video_capture qui a pour but de récupérer l'écran du téléphone connecté à l'ordinateur.

Test:
Ce module a été testé sur Linus avec CPU AMD de série 3000 et GPU Nvidia série 20

Classe:
    - Screen_video_capture : classe qui a pour but de récupérer l'écran du téléphone connecté à l'ordinateur

Dépendances:
    - cv2 (openCV)
    - numpy
    - scrcpy
    - adbutils
    - time
"""

import cv2
import numpy as np
import scrcpy
from adbutils import adb
import time
from use_fonction.configuration.fenetre_def import hauteur_capture


#sudo apt install adb
#pip install scrcpy-client

class Screen_video_capture:
    """
    Classe qui a pour but de récupérer l'écran du téléphone connecté à l'ordinateur en utilisant scrcpy.

    Attributs:
        frame (np.array): dernière image enregistrer de l'écran du téléphone

    Méthodes:
        on_frame(frame): Mais à jour l'attributs frame.
        get_screen(): Renvoie l'attributs frame après avoir été mis en taille désirée
    """
    def __init__(self):
        """
        Constructeur de la classe Screen_video_capture.
        """
        self.hauteur_desirer_capture = hauteur_capture
        self.frame=np.zeros((10,10,3))
        self.client = scrcpy.Client(device="DEVICE SERIAL")
        adb.connect("127.0.0.1:5555")
        self.client = scrcpy.Client(device=adb.device_list()[0])
        print(adb.device_list())
        self.client.add_listener(scrcpy.EVENT_FRAME, self.on_frame)
        self.client.start(threaded=True)
        time.sleep(1)



    def on_frame(self,frame):
        """
        Permet de configurer la fenêtre capturé par le programme

        Paramètres::
            frame (np.array): modifie l'attributs frame de la classe Screen_video_capture.
        """
        if frame is not None:
            self.frame=frame
            # print(np.shape(frame))
            # print(np.shape(self.frame))

    def get_screen(self):
        """
        Renvoie l'attributs frame après avoir été mis en taille désirée. Cette attributs correspond à la dernière capture enregistré du téléphone.
        """
        img = self.frame
        largeur = int(img.shape[1])
        hauteur = int(img.shape[0])
        self.facteur_echelle = self.hauteur_desirer_capture/hauteur

        largeur = int(largeur * self.facteur_echelle)
        hauteur = self.hauteur_desirer_capture

        img = cv2.resize(img, (largeur, hauteur))

        # Convertir en format couleur OpenCV
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        return frame
    
    def dev_click_scrcpy(self,x,y):
        pos_x=x/self.facteur_echelle
        pos_y=y/self.facteur_echelle
        # Mousedown
        self.client.control.touch(pos_x, pos_y, scrcpy.ACTION_DOWN)
        # Mouseup
        self.client.control.touch(pos_x, pos_y, scrcpy.ACTION_UP)