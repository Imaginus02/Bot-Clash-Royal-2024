"""
Nom du fichier: py_game_setup.py
Auteur: Étienne-Théodore PRIN
Date: 2024-02-02

Description:
Ce module définie la classe Screen_UI qui a pour but de créer une interface pour visualiser le fonctionnement des objets du projets.

Classe:
    - Screen_analyse : classe qui a pour but de créer une interface pour visualiser le fonctionnement des objets du projets.

Dépendances:
    - pygame
"""

import pygame

class Screen_UI:
    """
    Classe qui a pour but d'analyser une image du jeu Clash Royal pour en donner l'état.

    Méthodes:
        public:
        update_game(img, state): Fonction qui met à jour l'interface avec l'image du jeu et l'état du jeu.
        end_ui() : fonction fermant l'interface
        private:
        update_visible_state(state): Fonction qui met à jour la partie état de l'interface.
    """
    def __init__(self,x_size,y_size):
        """
        Créer un objet permettant de créer une interface pour visualiser le fonctionnement des objets du projets.

        Args:
            x_size : largeur des images du jeu clash royal qui seront fournies
            y_size : hauteur des images du jeu clash royal qui seront fournies

        Returns:
            None
        """
        pygame.init()
        self.window_size = x_size+230, y_size+30
        self.x = x_size
        self.y = y_size
        self.couleur_fond = (0, 0, 0)  # Noir
        self.window = pygame.display.set_mode(self.window_size)
        self.font = pygame.font.SysFont("arial", 20)
        self.font_state = pygame.font.SysFont("arial", 18)
        self.white = (255,255,255)

    def update_game(self, img, state):
        """
        Met à jour l'UI

        Args:
            img : image du jeu clash royal
            state : état correspond à l'image du jeu clash royal

        Returns:
            None
        """
        self.window.fill(self.couleur_fond)
        image_pygame = pygame.surfarray.make_surface(img.swapaxes(0, 1))
        self.window.blit(image_pygame, (30, 30))
        indice_bas_hors_game = 725
        text_0 = self.font.render("0     size : ["+str(self.x-30)+","+str(self.y)+"]", True, self.white)
        text_x = self.font.render(str(self.x), True, self.white)
        text_y = self.font.render(str(self.y), True, self.white)
        m_x, m_y = pygame.mouse.get_pos()
        m_x=min(max(m_x-30,0),self.x)
        m_y=min(max(m_y-30,0),self.y)
        text_pos = self.font.render(" mouse pos :"+str([m_x,m_y]), True, self.white)
        text_indice_bas_hors_game = self.font.render(str(indice_bas_hors_game), True, self.white)
        self.window.blit(text_0, (0, 0))
        self.window.blit(text_x, (self.x, 0))
        self.window.blit(text_y, (0, self.y))
        self.window.blit(text_indice_bas_hors_game, (0, indice_bas_hors_game+30))
        self.window.blit(text_pos, (200, 0))
        self.update_visible_state(state)
        pygame.display.flip()

    def update_visible_state(self,state):
        """
        Met à jour l'état de l'image indiqué par l'UI

        Args:
            state : état correspond à l'image du jeu clash royal affiché par l'UI

        Returns:
            None
        """
        text_state_0 = self.font.render(" | state_info", True, self.white)
        self.window.blit(text_state_0, (self.x + 30, 0))
        i=1
        if state[0]==True:
            text_state_1 = self.font_state.render("Game : True", True, (255, 255, 255))
            self.window.blit(text_state_1, (self.x + 35, 30 + i*25))
            for part_state in state[1:]:
                i+=1
                if part_state[0] == 1:
                    # Créer une surface avec canal alpha
                    x_l = part_state[3][0]
                    y_l = part_state[3][1]
                    x = 30 + part_state[1][0] - int(x_l/2)
                    y = 30 + part_state[1][1] - int(y_l/2)
                    pygame.draw.rect(self.window, self.white, (x, y, x_l, y_l), 2)
                    
                text_part_state = self.font_state.render(str(part_state[1])+"  "+str(part_state[2]), True, (255, 255, 255))
                self.window.blit(text_part_state, (self.x + 35, 30 + i*25))
        else:
            text_state_1 = self.font_state.render("Game : False", True, (255, 255, 255))
            self.window.blit(text_state_1, (self.x + 35, 30 + i*25))

    def end_ui(self):
        """
        Ferme l'interface

        Args:
            None

        Returns:
            None
        """
        pygame.quit()