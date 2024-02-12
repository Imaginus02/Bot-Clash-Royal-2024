"""
Nom du fichier: dev_to_game_click_linux.py
Auteur: Étienne-Théodore PRIN
Date: 2024-02-02

Description:
Ce module définie la classe controller qui a pour but de transmettre une action au jeu clash royal pour linux.

Classe:
    - controller : classe qui a pour but de transmettre une action au jeu clash royal.

Dépendances:
"""

class controller():
    """
    classe qui a pour but de transmettre une action au jeu clash royal.

    Méthodes:
        public:
        click(x,y): Click à l'endroit du jeu correspondant à l'endroit x,y du jeu sur l'image capturé du jeu.
        do_action(action) : reproduit l'action demandé en cliquant sur la carte désiré puis l'emplacement voulu sur le terrain.
            action a la forme : [index_de_la_carte(int),position_ou_placer([x(int),y(int)])]
    """
    def __init__(self,Screen_video_capture):
        """
        Créer un objet qui a pour but de transmettre une action au jeu clash royal.

        Args:
            Screen_video_capture : Objet qui permet de capturer les images du jeu clash royal et qui connait donc la position de la fenêtre de jeu.

        Returns:
            None
        """
        self.action_pos = {0:[171,743],
                           1:[243,738],
                           2:[333,744],
                           3:[408,756]}
        self.Screen_video_capture=Screen_video_capture

    def click(self,x ,y):
        """
        Effectue un click sur la fenêtre du jeu clash royal correspondant à la position x,y de l'image capturé du jeu

        Args:
            x,y : position de l'image capturé du jeu où l'on souhaite effectué un click

        Returns:
            None
        """
        self.Screen_video_capture.dev_click_scrcpy(x,y)

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
        x=self.action_pos[action[0]][0]
        y=self.action_pos[action[0]][1]
        self.click(x,y)
        x=action[1][0]
        y=action[1][1]
        self.click(x,y)