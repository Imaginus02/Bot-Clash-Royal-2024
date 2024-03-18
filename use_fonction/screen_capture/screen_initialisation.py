"""
Nom du fichier: screen_initialisation.py
Auteur: Étienne-Théodore PRIN
Date: 2024-02-02

Description:
Fonction qui permet d'initialiser la classe Screen_video_capture en fonction de l'os

fonction:
    - screen_initialisation() : fonction qui permet d'initialiser la classe Screen_video_capture en fonction de l'os

Dépendances:
    - sys
"""

import sys

def screen_initialisation():
    print("OS choosed : ",sys.platform)
    if sys.platform == "linux" or sys.platform == "linux2":
        # Importations spécifiques à Linux
        from use_fonction.screen_capture.capture_linux import Screen_video_capture
    elif sys.platform == "darwin":
        # Importations spécifiques à macOS
        from use_fonction.screen_capture.capture_mac import Screen_video_capture
    elif sys.platform == "win32":
        # Importations spécifiques à Windows
        from use_fonction.screen_capture.capture_windows import Screen_video_capture
        # from use_fonction.screen_capture.capture_linux import Screen_video_capture
    windows_capture = Screen_video_capture()
    return windows_capture