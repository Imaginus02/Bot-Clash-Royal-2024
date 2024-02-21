# Bot-Clash-Royal

Ce projet a pour but de poser une base pour permettre le développement d'un bot pour le jeu clash royal.

## Fonctionnement

Le programme fonctionne avec différents objets discutant entre eux selon le graphique suivant:
![graphique](Graphe_fonctionnement.png)
Les différents objets ont les objectifs suivant:
-Windows Capture : Enregistrer la fenêtre de jeu
-Screen analyse : renvoie l'état du jeu correspond à une capture
-Screen UI : créer une interface pour voir l'état et le jeu en cours
-Bot_ia : qui choisis une action en fonction de l'état
-Controller : Effectue l'action demandé en cliquant aux endroits désiré sur le jeu

## Prerequis

Pour récupérer la fenêtre de jeu sur ordinateur on passe par un émulateur pour Windows et Mac.

Pour Linux, il faut brancher le smartphone à l'ordinateur pour utiliser scrcpy.
[(Website-Scrcpy)](https://github.com/Genymobile/scrcpy/)
L'utilisation de scrcpy demande une étape d'initialisation sur le téléphone puisque qu'il faut activer le débogage USB.
[(Tuto activation débogage usb)](https://developer.android.com/studio/debug/dev-options?hl=fr#enable)

## Dépendances

Pour faire tourner ce programme il faut avoir installer les dépendances suivantes :

```
pip install sys pynput time cv2 numpy math pygame os ultralytics matplotlib
```
Il faut aussi installer PyTorch à l'aide de la ligne de commande trouvable [sur ce site en indiquant sa configuration](https://pytorch.org/get-started/locally/)


pour Linux il faut rajouter les commandes suivantes :
```
pip install scrcpy-client
sudo apt install adb
```
pour windows et mac:
```
pip install pygetwindow mss
```

## Initialisation

Avant le premier lancement il faut indiquer le chemin du dossier use_function dans le fichier use_fonction.configuration.p2p.py sans oublier de rajouter / à la fin

L'application devrait réussir à fonctionner au premier lancement cependant certaine partie de comparaison pixel par pixel pour évaluer les cartes disponibles,
l'état des tours ainsi que la quantité d'elixir disponible risque de demander une initialisation plus poussé.

### Comparaison pix to pix

La classification des cartes, de l'état des tours et de la quantité d'elixir ce fait pour des comparaison pixel par pixel dans des zones d'intérêts selectionnées. 
Il faut donc indiquer les zones dans le fichier use_fonction.configuration.p2p.py, ce dernier sert aussi à indiquer les chemins des précédents réseaux.

Pour créer les images pour les comparaisons p2p, nous avons le code vignette_creation.py et pour trouver les ROI nous avons vignette_find_roi.py du dossier vignette_creation

## Réentrainement Yolo


## Auteur

* **Étienne-Thédore PRIN** - [Website](https://prin.dev/)
