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

class bot():
    """
    classe qui a pour but de choisir l'action à effectuer en fonction de l'état de la partie clash royal.

    Méthodes:
        public:
        get_action(state) : renvoie l'action préconisé par le bot
            sous la forme [] si aucune action est prise ou
            [index_de_la_carte_à_poser(int),position_ou_placer([x(int),y(int)])]
        private:
        find_new_ennemies_troops(state): regarde si une nouvelle unité à été posée et laquelle
        create_list_card(state) : traduis le nom des cartes de l'état en indice d'unité donnée par le dictionnaire dict_trad donnée dans matrice_def.py

    """
    def __init__(self):
        """
        Créer un objet qui a pour but de choisir l'action à effectuer en fonction de l'état de la partie clash royal.

        Args:
            None

        Returns:
            None
        """
        self.previous_state=0
        self.matrice_choix=matrice_choix_def_response
        self.dict_trad=dict_trad
        self.elixir_price=elixir_price
        self.dictionnaire_translation=dictionnaire_translation
        self.card_dictionnary=card_dictionnary
        print(matrice_choix_def_response)
        self.p_time=time.time()

    def get_action(self, state):
        """
        Renvoie l'action préconisé par le bot

        Args:
            state : l'état du jeu à l'instant t

        Returns:
            action : sous la forme [] si aucune action est prise ou
                [index_de_la_carte_à_poser(int),position_ou_placer([x(int),y(int)])] si une carte doit être joué
        """
        action = 0
        if state[0]:
            diain = self.find_new_ennemies_troops(state)
            print(diain)
            if diain[0]:
                elixir_restant = state[1][2]
                index_troops=self.dict_trad[diain[3]]
                list_choices=self.matrice_choix[index_troops]
                list_card=self.create_list_card(state)
                for i in list_choices:
                    if self.elixir_price[i]<elixir_restant and i in list_card:
                        if diain[1]>220:
                            # time.sleep(5)
                            return [list_card.index(i),[339,548]]
                        if diain[1]<220:
                            # time.sleep(5)
                            return [list_card.index(i),[104,546]]
                print("action to be determined")
                print(elixir_restant)
                print(i)
                # time.sleep(5)
                return []
        return []
    
    def find_new_ennemies_troops(self, state):
        """
        Traduis le nom des cartes de l'état en indice d'unité donnée par le dictionnaire dict_trad donnée dans matrice_def.py

        Args:
            state : l'état du jeu à l'instant t

        Returns:
            state : [False]: si aucune nouvelle unité est détecté
                    [True,x,y,nom_de_l'unité_sans_couleur]
        """
        print(state)
        a_time=time.time()
        troops = None
        x,y=0,0
        if len(state)>9 and a_time-self.p_time>2:
            for i in state[10:]:
                if i[2]=='horloge_red':
                    x=int(i[1][0])
                    y=int(i[1][1])
                    self.p_time=a_time
            for i in state[10:]:
                if i[2]!='horloge_red' and i[2]!='msg' and i[2]!='horloge_blue':
                    x_i=int(i[1][0])
                    y_i=int(i[1][1])-10
                    d=math.sqrt(x_i*x_i+y_i*y_i)
                    min_d=1500
                    if d<min_d and d>2:
                        min_d=d
                        troops = i[2]
            if x!=0:
                print(troops)
                return [True,x,y,self.dictionnaire_translation[troops]]         
        return [False]

    def create_list_card(self,state):
        """
        traduis le nom des cartes de l'état en indice d'unité donnée par le dictionnaire dict_trad donnée dans matrice_def.py

        Args:
            state : l'état du jeu à l'instant t

        Returns:
            list_card : liste de quatre entiers indiquant les indices des unités jouable.
        """
        list_card=[]
        for i in state[6:10]:
            print(i[2])
            list_card.append(self.dict_trad[self.card_dictionnary[i[2]]])
        return list_card