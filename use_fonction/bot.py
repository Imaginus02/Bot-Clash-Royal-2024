"""
Nom du fichier: bot.py
Auteur: Étienne-Théodore PRIN
Date: 2024-02-02

Description:
Ce module définie la classe bot qui a pour but de choisir l'action à effectuer en fonction de l'état de la partie clash royal.

Classe:
    - bot : classe qui a pour but de choisir l'action à effectuer en fonction de l'état de la partie clash royal.

Dépendances:
    - math
    - time
    - matrice_def (définition de matrice constante et de dictionnaire utilisé pour effectuer les choix )
"""

from use_fonction.configuration.matrice_def import matrice_choix_def_response,dict_trad,elixir_price,dictionnaire_translation,card_dictionnary
import time
import math
import random

class bot():
    """
    classe qui a pour but de choisir l'action à effectuer en fonction de l'état de la partie clash royal.

    Méthodes:
        public:
        get_action(state) : renvoie l'action préconisé par le bot
            sous la forme [] si aucune action est prise ou
            [index_de_la_carte_à_poser(int),position_ou_placer([x(int),y(int)])]
        private:

    """
    def __init__(self):
        """
        Créer un objet qui a pour but de choisir l'action à effectuer en fonction de l'état de la partie clash royal.

        Args:
            None

        Returns:
            None
        """

    def get_action(self, state):
        """
        Renvoie l'action préconisé par le bot

        Args:
            state : l'état du jeu à l'instant t

        Returns:
            action : sous la forme [] si aucune action est prise ou
                [index_de_la_carte_à_poser(int),position_ou_placer([x(int),y(int)])] si une carte doit être joué
        """
        # Examples of state value:
        #[True,[0,"elixir",5],4*[0,"carte",carte.str],x*[1,[pos],"nom_objet",[w,h]]]
        #
        #[True, [0, 'elixir :', 4], [1, [292, 575], 'destroyed tower', [46, 61]], 
        #[1, [108, 73], 'destroyed tower', [49, 65]], [1, [80, 75], 'destroyed tower', [46, 55]], [1, [282, 76], 'destroyed tower', [43, 51]], [0, 'carte 0', 0], [0, 'carte 1', 'geant_vignette.jpg'], [0, 'carte 2', 'geant_vignette.jpg'], [0, 'carte 3', 0], [1, [90, 29], 'fleches', [177, 40]], [1, [334, 367], 'geant', [27, 38]], [1, [349, 350], 'geant', [28, 38]], [1, [328, 360], 'geant', [30, 33]], [1, [334, 339], 'geant', [30, 30]], [1, [351, 322], 'geant', [27, 36]], [1, [338, 312], 'info-message', [31, 41]], [1, [347, 352], 'chevalier', [69, 62]], [1, [369, 342], 'geant', [35, 33]], 
        #[1, [343, 318], 'geant', [39, 46]]]
        
        
        action = 0
        if state[0]:
            elixir = state[1][2]
            temp = [i for i in state if type(i) == list]
            cards = [i for i in temp if i[0] == 0 and 'carte' in i[1]]
            entities = [i for i in temp if i[0] == 1]
            #print(cards)
            if elixir>=5:
                nombre_aleatoire = random.randint(0, 3)
                return [nombre_aleatoire,[339,548]]
        return []
