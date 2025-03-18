"""
Nom du fichier: main.py
Auteur: Étienne-Théodore PRIN
Date: 2024-02-02

Description:
Ce module fait le lien entre toutes les différentes classes du projet Bot clash Royal.
Il initialise les classes puis les fait interargir entre elles dans la boucle while.

Dépendances:
    - pygame
    - time
    - nécessite la création du CNN vgg10 (initialisable avec ai_creation.ia_ingame.ia_ingame_learning.py)
    - nécessite la création d'un yolo avec le code train_yolo.py et d'une base de donnée
    - classes trouvable dans le dossier use_fonction
"""

import pygame

from use_fonction.screen_capture.screen_initialisation import screen_initialisation
from use_fonction.controller.controller_initialisation import controller_initialisation
from use_fonction.py_game_setup import Screen_UI
from use_fonction.screen_analyse import Screen_analyse
from use_fonction.bot import bot

import time

# Créer système de capture video
windows_capture = screen_initialisation()

# Créer une fenêtre de la taille de l'image
image = windows_capture.get_screen()
screen_ui = Screen_UI(image.shape[1], image.shape[0])

# créer l'analyseur d'image
analyse = Screen_analyse()

# créer souris virtuelle
mouse_v = controller_initialisation(windows_capture)

# créer bot
bot_ia = bot()
clock = pygame.time.Clock()
running = True
action = []
while running:
    old = time.time()
    # print(old)
    image = windows_capture.get_screen()
    state = analyse.get_state(image)
    # print(state)
    if state[0] == True:
        action = bot_ia.get_action(state, image)

    if action!=[]:
        #print(action)
        time.sleep(1)
        mouse_v.do_action(action)
        # time.sleep(5)

    screen_ui.update_game(image,state)
    now = time.time()
    # time.sleep(0.3)
    # print((now - old))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # bouton gauche
                m_x, m_y = pygame.mouse.get_pos()
                mouse_v.click(m_x, m_y)
    clock.tick(60)
        

screen_ui.end_ui()