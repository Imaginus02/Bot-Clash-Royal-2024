"""
Nom du fichier: dev_to_game_click.py
Auteur: Étienne-Théodore PRIN
Date: 2024-02-02

Description:
Ce module définie la classe controller qui a pour but de transmettre une action au jeu clash royal.

Classe:
    - controller : classe qui a pour but de transmettre une action au jeu clash royal.

Dépendances:
    - pynput
    - time
"""

from pynput.mouse import Controller, Button
import time

class controller():
    """
    classe qui a pour but de transmettre une action au jeu clash royal.

    Méthodes:
        public:
        click(x,y): Click à l'endroit du jeu correspondant à l'endroit x,y du jeu sur l'image capturé du jeu.
        do_action(action) : reproduit l'action demandé en cliquant sur la carte désiré puis l'emplacement voulu sur le terrain.
            action a la forme : [index_de_la_carte(int),position_ou_placer([x(int),y(int)])]
        get_position() : renvoie la position de la sourie sur l'écran
    """
    def __init__(self,Screen_video_capture):
        """
        Créer un objet qui a pour but de transmettre une action au jeu clash royal.

        Args:
            Screen_video_capture : Objet qui permet de capturer les images du jeu clash royal et qui connait donc la position de la fenêtre de jeu.

        Returns:
            None
        """
        self.mouse = Controller()
        self.action_pos = {0:[171,743],
                           1:[243,738],
                           2:[333,744],
                           3:[408,756]}
        self.Screen_video_capture=Screen_video_capture

    def click(self,x ,y ):
        """
        Effectue un click sur la fenêtre du jeu clash royal correspondant à la position x,y de l'image capturé du jeu

        Args:
            x,y : position de l'image capturé du jeu où l'on souhaite effectué un click

        Returns:
            None
        """
        position = self.mouse.position
        # Déplacer la souris à une position spécifique
        x-=30
        y-=30
        self.mouse.position = self.Screen_video_capture.dev_position_to_screen(x,y)
        # Clic gauche
        self.mouse.click(Button.left, 1)
        self.mouse.click(Button.left, 1)
        self.mouse.position = position
        # self.mouse.click(Button.left, 1)

    def do_action(self,action):
        """
        Effectue l'action demandé

        Args:
            action(list) : liste indiquant la carte et l'endroit où elle doit être posée
                    action a la forme : [index_de_la_carte(int),position_ou_placer([x(int),y(int)])]

        Returns:
            None
        """
        # action = [int([0-3],pos[int(x),int(y)])]
        position = self.mouse.position
        print("action en lancement")
        self.mouse.position = self.Screen_video_capture.dev_position_to_screen(3,3)
        self.mouse.click(Button.left, 1)
        x=self.action_pos[action[0]][0]
        y=self.action_pos[action[0]][1]
        print(x,y)
        self.mouse.position = self.Screen_video_capture.dev_position_to_screen(x,y)
        print("move to :",self.Screen_video_capture.dev_position_to_screen(x,y))
        self.mouse.click(Button.left, 1)
        time.sleep(0.2)
        x=action[1][0]
        y=action[1][1]
        self.mouse.position = self.Screen_video_capture.dev_position_to_screen(x,y)
        print("move to :",self.Screen_video_capture.dev_position_to_screen(x,y))
        self.mouse.click(Button.left, 1)
        self.mouse.position = position
        self.mouse.click(Button.left, 1)

    def get_position(self):
        """
        Renvoie la position de la sourie

        Args:
            None

        Returns:
            None
        """
        return self.mouse.position