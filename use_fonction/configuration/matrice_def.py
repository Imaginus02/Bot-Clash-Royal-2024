"""
Nom du fichier: matrice_def.py
Auteur: Étienne-Théodore PRIN
Date: 2024-02-02

Description:
Ce module définie des variables utilisées dans différentes parties du projets.
Il est utilisé pour créer la première logique du bot

Variables:
    dict_trad: dictionnaire permettant d'avoir l'index des différents unités pour les autres variables (elixir_price,matrice_choix_def_response)
    elixir_price: liste indiquant la coût en elixir des unités en fonction de leur index donnée par dict_trad
    dictionnaire_translation: dictionnaire traduisant la sortie la sortie du yolo pour être utilisé par dict_trad
    matrice_choix_def_response: matrice indiquant les unités interessante à jouer contre chaque unité
    card_dictionnary: dictionnaire traduisant les noms des fichiers des vignettes des cartes
"""

dict_trad={
    "chevalier":0,
    "archers":1,
    "gargouilles":2,
    "flèches":3,
    "fireball":4,
    "géant":5,
    "mini_PK":6,
    "mousquetaire":7
}
elixir_price=[3,3,3,3,4,5,4,4]
dictionnaire_translation={'archere_blue':"archers", 
                          'archere_red':"archers", 
                          'chevalier_blue':"chevalier", 
                          'chevalier_red':"chevalier", 
                          'fire_ball':'fire_ball', 
                          'fleches':'fleches', 
                          'gargouille_blue':"gargouilles", 
                          'gargouille_red':"gargouilles", 
                          'geant_blue':"géant", 
                          'geant_red':"géant", 
                          'horloge_blue':'horloge', 
                          'horloge_red':'horloge', 
                          'mousquetaire_blue':'mousquetaire', 
                          'mousquetaire_red':'mousquetaire', 
                          'msg':'msg', 
                          'pk_blue':'mini_PK', 
                          'pk_red':'mini_PK'}
matrice_choix_def_response=[
    [6,7,0,2,1,3,4,5],
    [0,7,3,4,2,1,6,5],
    [0,7,3,4,2,1,6,5],
    [0,1,2,3,4,5,6,7],
    [0,1,2,3,4,5,6,7],
    [6,7,1,2,0,3,4,5],
    [1,2,0,6,7,3,4,5],
    [6,5,1,0,2,3,4,5],
]
card_dictionnary={
    "archere_vignette.jpg":"archers",
    "chevalier_vignette.jpg":"chevalier",
    "fireball_vignette.jpg":"fireball",
    "fleches_vignette.jpg":"flèches",
    "gargouilles_vignette.jpg":"gargouilles",
    "geant_vignette.jpg":"géant",
    "mousquetaire_vignette.jpg":"mousquetaire",
    "PK_vignette.jpg":"mini_PK"
}