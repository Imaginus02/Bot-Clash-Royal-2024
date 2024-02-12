# Bot-Clash-Royal

Ce projet a pour but de poser une base pour permettre le développement d'un bot pour le jeu clash royal.

## Fonctionnement

Le programme fonctionne avec différents objets discutant entre eux selon le graphique suivant:
![graphique](Graphe_fonctionnement.png)
Les différents objets ont les objectifs suivant:
Windows Capture : Enregistrer la fenêtre de jeu
Screen analyse : renvoie l'état du jeu correspond à une capture
Screen UI : créer une interface pour voir l'état et le jeu en cours
Bot_ia : qui choisis une action en fonction de l'état
Controller : Effectue l'action demandé en cliquant aux endroits désiré sur le jeu

## Prerequis

Pour récupérer la fenêtre de jeu sur ordinateur on passe par un émulateur pour Windows et Mac.

Pour Linux, il faut brancher le smartphone à l'ordinateur pour utiliser scrcpy.
[(Website-Scrcpy)](https://github.com/Genymobile/scrcpy/)
L'utilisation de scrcpy demande une étape d'initialisation sur le téléphone puisque qu'il faut activer le débogage USB.
[(Tuto activation débogage usb)](https://developer.android.com/studio/debug/dev-options?hl=fr#enable)

## Dépendances

Pour faire tourner ce programme il faut avoir installer les dépendances suivantes:

'''
pip install numpy
'''

## Auteur

* **Étienne-Thédore PRIN** - [Website](https://prin.dev/)
