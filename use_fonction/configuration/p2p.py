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

chemin_vgg10='ai_creation/ia_ingame/vgg10_model.pth'
chemin_yolo="F:/projet indus/use_fonction/v2.pt"
classes_yolo=['archere_blue', 
              'archere_red', 
              'chevalier_blue', 
              'chevalier_red', 
              'fire_ball', 
              'fleches', 
              'gargouille_blue', 
              'gargouille_red', 
              'geant_blue', 
              'geant_red', 
              'horloge_blue', 
              'horloge_red', 
              'mousquetaire_blue', 
              'mousquetaire_red', 
              'msg', 
              'pk_blue', 
              'pk_red']
ROI_cartes=[[106,673,63,80],
            [190,673,63,80],
            [275,673,63,80],
            [359,673,63,80]]
chemin_dossier_vignettes='F:/projet indus/use_fonction/vignettes'
ROI_elixir=[119,785,311,1]
ROI_tower=[[315,125,52,70],
           [80,125,52,70],
           [78,456,54,65],
           [313,456,54,65]]
chemin_dossier_tours='F:/projet indus/use_fonction/towers'