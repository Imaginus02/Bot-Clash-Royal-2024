"""
Nom du fichier: controller_initialisation.py
Auteur: Étienne-Théodore PRIN
Date: 2024-02-02

Description:
Fonction qui permet d'initialiser la classe controller en fonction de l'os

fonction:
    - controller_initialisation() : fonction qui permet d'initialiser la classe controller en fonction de l'os

Dépendances:
    - sys
"""

import sys

def controller_initialisation(windows_capture):
    print("OS choosed : ",sys.platform)
    if sys.platform == "linux" or sys.platform == "linux2":
        # Importations spécifiques à Linux
        from use_fonction.controller.dev_to_game_click_linux import controller
    elif sys.platform == "darwin":
        # Importations spécifiques à macOS
        from use_fonction.controller.dev_to_game_click import controller
    elif sys.platform == "win32":
        # Importations spécifiques à Windows
        from use_fonction.controller.dev_to_game_click import controller
        # from use_fonction.controller.dev_to_game_click_linux import controller
    controller_v = controller(windows_capture)
    return controller_v