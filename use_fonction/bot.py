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
    "squelette_vignette.jpg":3,
    "gobelin_vignette.jpg":2,
    "archere_vignette.jpg":3,
    "chevalier_vignette.jpg":3,
    "geant_vignette.jpg":5,
    "PK_vignette.jpg":4,
    "buche_vignette.jpg":2,
    "bat_vignette.jpg":2
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
        if blue_ratio > gold_ratio and blue_ratio > 0.3:
            team = 'enemy'  # Enemy team (blue health bars)
        elif gold_ratio > 0.01:  # Lower threshold to catch more gold
            team = 'friendly'  # Your team (gold health bars)
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
        self.compteur = 0
        """
        Créer un objet qui a pour but de choisir l'action à effectuer en fonction de l'état de la partie clash royal.

        Args:
            None

        Returns:
            None
        """
        self.compteur = 0
        self.last_card_played = None
        self.elixir_threshold = 6  # Default threshold for playing cards
        self.defense_mode = False
        self.defense_timer = 0
        self.attack_queue = []
        self.last_defense_time = 0
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
        
        self.compteur += 1
        
        # If no state, return empty action
        if not state[0]:
            return []
            
        # Parse game state
        elixir, towers, cards, entities = parse_state(state)
        teams = categorize_teams(entities, image)
        
        # Convert teams list to a dictionary for easier access
        entity_teams = {}
        for i, (entity_id, team) in enumerate(teams):
            entity_teams[entity_id] = team
        
        # Extract friendly and enemy entities
        friendly_entities = [entities[i] for i, (entity_id, team) in enumerate(teams) if team == "friendly"]
        enemy_entities = [entities[i] for i, (entity_id, team) in enumerate(teams) if team == "enemy"]
        
        # Check tower health
        our_towers = [tower for tower in towers if tower[1][1] > 400] # Assume towers under y=400 are ours
        enemy_towers = [tower for tower in towers if tower[1][1] < 400] # Assume towers above y=400 are enemies
        
        #print("our_towers",our_towers)
        #print("enemy_towers",enemy_towers)
        # Bot logic
        action = self.decide_action(elixir, our_towers, enemy_towers, cards, friendly_entities, enemy_entities)
        return action

    def decide_action(self, elixir, our_towers, enemy_towers, cards, friendly_entities, enemy_entities):
        # Reset attack queue if needed
        if self.compteur % 600 == 0:  # Every ~10 seconds
            self.attack_queue = []
        
        # Check if we need to defend
        if self.should_defend(enemy_entities, our_towers) and not self.defense_mode:
            #print("defense")
            self.defense_mode = True
            self.defense_timer = self.compteur + 15  # Stay in defense mode for ~2.5 seconds
            self.last_defense_time = self.compteur
        
        # Check if we can exit defense mode
        if self.defense_mode and self.compteur >= self.defense_timer:
            self.defense_mode = False
        elif self.defense_mode:
            print("Remaining in defense mode for {} frames".format(self.defense_timer - self.compteur))
            pass
        
        # If we're in defense mode, prioritize defense
        if self.defense_mode:
            defense_action = self.defend(elixir, enemy_entities, our_towers, cards)
            if defense_action:
                return defense_action
        
        # If we have enough elixir and not in immediate danger, check for attack opportunities
        if elixir >= self.elixir_threshold and not self.defense_mode:
            #print("attack")
            # If we have attack queued, execute the next one
            if self.attack_queue:
                next_attack = self.attack_queue.pop(0)
                card_index, position = next_attack
                #print(card_index)
                #print("Next attack:", cards[card_index][1], position)
                # Verify the card is available
                if card_index < len(cards) and elixir >= prix_cartes[cards[card_index][2]]:  # Ensure we have enough elixir
                    self.last_card_played = cards[card_index][1]
                    return [card_index, position]
            
            # Otherwise, decide on a new attack
            return self.attack(elixir, enemy_towers, cards, friendly_entities)
        
        # If we have low elixir or just defended, wait
        if elixir < 5 or (self.compteur - self.last_defense_time) < 60:
            return []
        
        # Default action: wait and accumulate elixir
        return []
    
    def should_defend(self, enemy_entities, our_towers):
        # Determine if we're under significant threat
        
        # Check if enemies are close to our towers
        for tower in our_towers:
            tower_x, tower_y = tower[1][0], tower[1][1]
            
            for enemy in enemy_entities:
                enemy_id, (enemy_x, enemy_y), enemy_type, _ = enemy
                
                # Calculate distance to tower
                distance = ((enemy_x - tower_x) ** 2 + (enemy_y - tower_y) ** 2) ** 0.5
                
                # If enemy is close to our tower, we should defend
                if distance < 150:  # Adjust threshold as needed
                    return True
        
        return False
    
    def defend(self, elixir, enemy_entities, our_towers, cards):
        # Basic defense logic
        if not enemy_entities or elixir < 3:
            return []
        
        # Find the most threatening enemy (closest to our towers)
        closest_enemy = None
        min_distance = float('inf')
        
        for tower in our_towers:
            tower_x, tower_y = tower[1][0], tower[1][0]
            
            for enemy in enemy_entities:
                enemy_id, (enemy_x, enemy_y), enemy_type, _ = enemy
                
                # Calculate distance to tower
                distance = ((enemy_x - tower_x) ** 2 + (enemy_y - tower_y) ** 2) ** 0.5
                
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
        
        if closest_enemy:
            enemy_id, (enemy_x, enemy_y), enemy_type, _ = closest_enemy
            
            # Choose appropriate defender based on available cards
            defender_index = self.choose_defender(cards, enemy_type)
            
            if defender_index is not None:
                # Place defender between enemy and tower
                target_tower = min(our_towers, key=lambda t: ((t[1][0] - enemy_x) ** 2 + (t[1][1] - enemy_y) ** 2) ** 0.5)
                tower_x, tower_y = target_tower[1][0], target_tower[1][1]
                
                # Calculate midpoint between enemy and tower
                mid_x = (enemy_x + tower_x) // 2
                mid_y = (enemy_y + tower_y) // 2
                
                # Ensure within playable area
                mid_x = max(100, min(mid_x, 600))
                mid_y = max(100, min(mid_y, 600))
                
                self.last_card_played = cards[defender_index][1]
                return [defender_index, [mid_x, mid_y]]
        
        return []
    
    def choose_defender(self, cards, enemy_type):
        #print("Choosing defender for", enemy_type)
        # Map cards to indices
        card_indices = {cards[i][2]: i for i in range(len(cards))}
        #print("available cards",card_indices)
        
        # Prioritize defenders based on enemy type
        defenders_priority = []
        
        # Handle different enemy types with appropriate counters
        if "geant" in enemy_type.lower():
            defenders_priority = ["PK", "squelette", "gobelin", "archere"]
        elif "bat" in enemy_type.lower():
            defenders_priority = ["archere", "squelette", "gobelin", "chevalier"]
        elif "chevalier" in enemy_type.lower():
            defenders_priority = ["squelette", "gobelin", "PK", "archere"]
        elif "gobelin" in enemy_type.lower() or "squelette" in enemy_type.lower():
            defenders_priority = ["buche", "chevalier", "archere"]
        elif "zappy" in enemy_type.lower():
            defenders_priority = ["bat", "PK", "chevalier", "archere"]
        elif "mousquetaire" in enemy_type.lower():
            defenders_priority = ["squelette", "chevalier", "archere", "buche"]
        elif "valkyrie" in enemy_type.lower():
            defenders_priority = ["bat", "chevalier", "PK", "archere"]
        elif "squelette" in enemy_type.lower():
            defenders_priority = ["buche", "squeltte", "gobelin", "archere"]
        else:
            # Default priority
            defenders_priority = ["chevalier", "squelette", "gobelin", "archere", "PK", "buche"]
        
        # Find the first available defender from our priority list
        for defender in defenders_priority:
            if (defender+"_vignette.jpg") in card_indices:
                #print("Defending against", enemy_type, "with", defender)
                #print("Using card", cards[card_indices[defender+"_vignette.jpg"]][1])
                return card_indices[defender+ "_vignette.jpg"]
        
        # If none of our preferred defenders are available, use any card
        for i in range(len(cards)):
            return i
        
        return None
    
    def attack(self, elixir, enemy_towers, cards, friendly_entities):
        # Define attacking strategies
        
        # If elixir is high, we can try a push attack
        if elixir >= 8:
            return self.execute_push_attack(cards, enemy_towers)
        
        # If elixir is medium, try a split attack
        elif elixir >= 6:
            return self.execute_split_attack(cards, enemy_towers)
        
        # If elixir is lower, use cheaper cards or wait
        elif elixir >= 4:
            return self.execute_chip_attack(cards, enemy_towers)
        
        # Otherwise wait for more elixir
        return []
    
    def execute_push_attack(self, cards, enemy_towers):
        """Strong push with tank + support troops"""
        card_types = [card[2] for card in cards]
        #print("push attack card type",card_types)
        
        # Queue up a strong push
        target_tower = enemy_towers[0]  # Target the first enemy tower
        tower_x, tower_y = target_tower[1][0], target_tower[1][1]
        
        # Position slightly away from the tower
        attack_x = tower_x + (-100 if tower_x > 300 else 100)
        attack_y = tower_y + (-100 if tower_y > 300 else 100)
        
        # Check for tank cards
        if "geant_vignette.jpg" in card_types:
            tank_index = card_types.index("geant_vignette.jpg")
            self.attack_queue.append([tank_index, [attack_x, attack_y]])
            
            # Queue support troops
            if "archere_vignette.jpg" in card_types:
                support_index = card_types.index("archere_vignette.jpg")
                support_x = attack_x + 30
                support_y = attack_y + 30
                self.attack_queue.append([support_index, [support_x, support_y]])
            
            # Return the first action
            return self.attack_queue.pop(0)
            
        # If no tank, try a mini-tank
        elif "chevalier_vignette.jpg" in card_types:
            tank_index = card_types.index("chevalier_vignette.jpg")
            self.attack_queue.append([tank_index, [attack_x, attack_y]])
            
            # Queue support troops
            if "gobelin_vignette.jpg" in card_types or "squelette_vignette.jpg" in card_types:
                support_index = card_types.index("gobelin_vignette.jpg" if "gobelin_vignette.jpg" in card_types else "squelette_vignette.jpg")
                support_x = attack_x + 30
                support_y = attack_y + 30
                self.attack_queue.append([support_index, [support_x, support_y]])
            
            # Return the first action
            return self.attack_queue.pop(0)
        
        # Default to card 0 if no good options
        return [0, [attack_x, attack_y]]
    
    def execute_split_attack(self, cards, enemy_towers):
        """Split attack on two lanes to divide opponent's attention"""
        card_types = [card[2] for card in cards]
        #print("split attack",card_types)
        
        # Find mid-cost cards for split pushing
        split_candidates = []
        for i, card_type in enumerate(card_types):
            if card_type in ["chevalier_vignette.jpg", "archere_vignette.jpg", "gobelin_vignette.jpg"]:
                split_candidates.append(i)
        
        if len(split_candidates) >= 2:
            # Get two lanes for attack
            left_lane = [200, 400]
            right_lane = [500, 400]
            
            # Queue up split push
            self.attack_queue.append([split_candidates[0], left_lane])
            self.attack_queue.append([split_candidates[1], right_lane])
            
            # Return the first action
            return self.attack_queue.pop(0)
        
        # Fall back to normal attack if not enough split cards
        return self.execute_chip_attack(cards, enemy_towers)
    
    def execute_chip_attack(self, cards, enemy_towers):
        """Chip damage with cheap cards"""
        card_types = [card[2] for card in cards]
        #print("chip attack cards type",card_types)
        
        # Find cheap cards for chip damage
        chip_candidates = []
        for i, card_type in enumerate(card_types):
            if card_type in ["gobelin_vignette.jpg", "squelette_vignette.jpg", "archere_vignette.jpg", "bat_vignette.jpg"]:
                chip_candidates.append(i)
        
        if chip_candidates:
            # Target tower
            target_tower = enemy_towers[0]
            tower_x, tower_y = target_tower[1][0], target_tower[1][1]
            
            # Position offset from tower
            attack_x = tower_x + (-80 if tower_x > 300 else 80)
            attack_y = tower_y + (-80 if tower_y > 300 else 80)
            
            # Choose a cheap card
            cheap_card_index = chip_candidates[0]
            
            return [cheap_card_index, [attack_x, attack_y]]
        
        # No good chip cards, wait for better opportunity
        return []
