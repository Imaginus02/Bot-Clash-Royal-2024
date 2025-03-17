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
import numpy as np
import cv2


prix_cartes = {
    "armee_squelette_vignette.jpg":3,
    "gobelin_a_lance_vignette.jpg":3,
    "archere_vignette.jpg":3,
    "chevalier_vignette.jpg":3,
    "geant_vignette.jpg":5,
    "PK_vignette.jpg":4,
    "buche_vignette.jpg":2,
    "chauvesouris_vignette.jpg":2
}

def parse_state(state):
                """
                Parse the game state to extract elixir, towers, cards, and entities.

                Args:
                    state : l'état du jeu à l'instant t

                Returns:
                    tuple : (elixir, towers, cards, entities)
                """
                elixir = state[1][2]
                temp = [i for i in state if type(i) == list]
                cards = [i for i in temp if i[0] == 0 and 'carte' in i[1]]
                entities = [i for i in temp if i[0] == 1]
                towers = [i for i in entities if 'destroyed tower' in i[2] or "alive tower" in i[2]]
                entities = [entity for entity in entities if entity not in towers]
                return elixir, towers, cards, entities


def categorize_teams(entities, image, debug=False):
    """
    Categorize each entity into red, blue, or none based on the dominant color in their bounding box.
    
    :param entities: List of entities, where each entity is represented as [id, [pos_x, pos_y], 'type', [w, h]]
    :param image: The image (frame) from the game where the entities are located
    :param debug: If True, display debug information and visualizations
    :return: A list of tuples containing the entity ID and its team ('red', 'blue', or 'none')
    """
    categorized_entities = []

    # It seems in your game, the health bars are:
    # - Gold/yellow for your team
    # - Blue for enemies
    # Let's modify the color ranges accordingly
    
    for entity in entities:
        entity_id, (pos_x, pos_y), entity_type, (w, h) = entity

        # Extract the bounding box region from the image
        # Calculate the top-left corner of the bounding box from the center coordinates
        top_left_x = pos_x - w // 2
        top_left_y = pos_y - h // 2

        # Extract the bounding box region from the image
        bbox = image[top_left_y:top_left_y + h, top_left_x:top_left_x + w]

        # Convert the bounding box to HSV color space for easier color detection
        hsv_bbox = cv2.cvtColor(bbox, cv2.COLOR_BGR2HSV)

        # Define color ranges for gold/yellow and blue in HSV
        # Gold/yellow health bars
        lower_gold = np.array([20, 100, 100])  # Gold/yellow range (adjust as needed)
        upper_gold = np.array([35, 255, 255])
        
        # Blue health bars
        lower_blue = np.array([90, 50, 50])  # Blue range (expanded to catch more blue tones)
        upper_blue = np.array([140, 255, 255])

        # Create masks for gold and blue colors
        gold_mask = cv2.inRange(hsv_bbox, lower_gold, upper_gold)
        blue_mask = cv2.inRange(hsv_bbox, lower_blue, upper_blue)

        # Count the number of gold and blue pixels in the bounding box
        gold_pixels = cv2.countNonZero(gold_mask)
        blue_pixels = cv2.countNonZero(blue_mask)

        # Calculate the proportion of gold and blue pixels relative to the bounding box size
        total_pixels = w * h
        gold_ratio = gold_pixels / total_pixels
        blue_ratio = blue_pixels / total_pixels

        # Determine the team based on the dominant color
        # Let's use the colors to determine the actual team
        if gold_ratio > blue_ratio and gold_ratio > 0.03:  # Lower threshold to catch more gold
            team = 'friendly'  # Your team (gold health bars)
        elif blue_ratio > gold_ratio and blue_ratio > 0.3:
            team = 'enemy'  # Enemy team (blue health bars)
        else:
            team = 'friendly'  # Default to friendly if no clear color is detected

        # Debugging output
        #debug = 1
        if debug:
            print(f"Entity {entity_id}: Gold pixels = {gold_pixels} ({gold_ratio:.2f}), Blue pixels = {blue_pixels} ({blue_ratio:.2f}), Team = {team}")
            
            # Draw bounding box
            debug_image = image.copy()
            color = (0, 255, 0)  # Green box
            if team == 'friendly':
                color = (0, 215, 255)  # Yellow box for friendly
            elif team == 'enemy':
                color = (255, 0, 0)  # Red box for enemy
                
            cv2.rectangle(debug_image, (pos_x, pos_y), (pos_x + w, pos_y + h), color, 2)
            cv2.putText(debug_image, team, (pos_x, pos_y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # Show images
            cv2.imshow(f"Entity {entity_id} - Detection", debug_image)
            cv2.imshow(f"Entity {entity_id} - Gold Mask", gold_mask)
            cv2.imshow(f"Entity {entity_id} - Blue Mask", blue_mask)
            cv2.waitKey(500)  # Wait for 500ms instead of indefinitely
            cv2.destroyAllWindows()

        categorized_entities.append((entity_id, team))

    return categorized_entities


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
        self.coord_attaque = [[110,420],[365, 420]]

    def get_action(self, state, image):
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

            # Usage in the bot class
            elixir, towers, cards, entities = parse_state(state)
            #print(categorize_teams(entities, image))
            # if elixir>=5:
            #     nombre_aleatoire = random.randint(0, 3)
            #     return [nombre_aleatoire,[339,548]]
        return []
