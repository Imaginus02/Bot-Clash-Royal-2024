"""
Nom du fichier: p2p.py
Auteur: Étienne-Théodore PRIN
Date: 2024-02-02

Description:
Ce module définie des variables utilisées dans l'objet screen analysis.

Variables:
    chemin_vgg10: le chemin vers le model entrainé du vgg10
    chemin_yolo: le chemin vers le model entrainé du yolo
    classes_yolo: list des labels utilisé par le model yolo
    ROI_cartes: x,y,w,h des boundings boxes des cartes pour la détection pix to pix des cartes disponibles.
    chemin_dossier_vignettes: le chemin menant au dossier contenant les images des différentes cartes possibles
    ROI_elixir: x,y,w,h=1 pour la ligne permettant de calculer l'elixir de la partie.
         la bounding boxe doit être une ligne de 1 pixel de hauteur et faisant la longueur de la barre d'elixir
    ROI_tower: x,y,w,h des boundings boxes des tours pour la détection pix to pix de létat des tours
    chemin_dossier_tours : le chemin menant au dossier contenant les images des tours rouges et bleu en vie 
"""

import json
import yaml

chemin_use_fonction = 'F:/projet indus/use_fonction/'

chemin_vgg10='ai_creation/ia_ingame/vgg10_model_light.pth'
chemin_yolo=chemin_use_fonction+"v2.pt"

fichier_yaml = 'F:/projet indus final/Bot-Clash-Royal/use_fonction/configuration/data.yaml'
with open(fichier_yaml, 'r') as fichier:
    labels = yaml.safe_load(fichier)

classes_yolo=labels["names"]
# print(classes_yolo)

# Chemin vers votre fichier JSON
fichier_json = 'F:/projet indus final/Bot-Clash-Royal/use_fonction/configuration/roi_data.json'
with open(fichier_json, 'r') as fichier:
    roi_info = json.load(fichier)

ROI_cartes=roi_info["ROI_cartes"]
chemin_dossier_vignettes=chemin_use_fonction+"vignettes"
ROI_elixir=roi_info["ROI_elixir"]
ROI_tower=roi_info["ROI_tower"]
chemin_dossier_tours=chemin_use_fonction+"towers"