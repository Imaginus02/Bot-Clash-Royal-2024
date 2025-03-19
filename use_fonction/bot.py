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
import time


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
                entities = [i for i in temp if i[0] > 1]
                towers = [i for i in temp if i[0] == 1]
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
        bounding_offset = 10 #extends the bounding box to include the small red box on the ennemy
        top_left_x = pos_x - (w // 2)
        top_left_y = pos_y - (h // 2)

        # Extract the bounding box region from the image
        bbox = image[top_left_y-bounding_offset:top_left_y +h, top_left_x:top_left_x + w]

        # Convert the bounding box to HSV color space for easier color detection
        #rgb_box = cv2.cvtColor(bbox, cv2.COLOR_BGR2RGB)
        rgb_box = bbox
        # Blue
        lower_blue = np.array([20, 80, 160]) 
        upper_blue = np.array([100, 170, 255])

        # Red 
        lower_red = np.array([120, 10, 35])
        upper_red = np.array([255, 90, 100])
        

        # Create masks for Red and Blue colors
        blue_mask = cv2.inRange(rgb_box, lower_blue, upper_blue)
        red_mask = cv2.inRange(rgb_box, lower_red, upper_red)
        green_space = np.full((blue_mask.shape[0], 10), 255, dtype=np.uint8)
        mask_combined = cv2.hconcat([blue_mask, green_space, red_mask])
        cv2.imshow("bbox", mask_combined)
        # Count the number of Red and Blue pixels in the bounding box
        blue_pixels = cv2.countNonZero(blue_mask)
        red_pixels = cv2.countNonZero(red_mask)

        # Calculate the proportion of Red and blue pixels relative to the bounding box size
        
        blue_ratio = blue_pixels / blue_mask.size
        red_ratio = red_pixels / red_mask.size

        # Determine the team based on the dominant color
        # Let's use the colors to determine the actual team
        if red_ratio > blue_ratio and red_ratio > 0.05:
            team = 'enemy'  # Enemy team (blue health bars)
        elif blue_ratio > red_ratio and blue_ratio > 0.05:  # Lower threshold to catch more gold
            team = 'friendly'  # Your team (gold health bars)
        else:
            team = 'enemy'
        if entity_id == 3 and debug:  # Only show for the first entity for debugging purposes
            height, width = bbox.shape[:2]
            aspect_ratio = width / height
            new_width = int(200 * aspect_ratio)
            resized_blue_mask = cv2.resize(blue_mask, (new_width, 200))  # Resize the blue mask image while keeping the aspect ratio
            resized_red_mask = cv2.resize(red_mask, (new_width, 200))  # Resize the red mask image while keeping the aspect ratio

            # Combine the two images side by side
            combined_mask = np.hstack((resized_blue_mask, resized_red_mask))

            cv2.imshow("bbox" + team, combined_mask)
            cv2.waitKey(100)
        # Debugging output
        #debug = 1
        if debug:
            print(f"Entity {entity_id}: Gold pixels = {blue_ratio} ({blue_ratio:.2f}), Blue pixels = {red_pixels} ({red_ratio:.2f}), Team = {team}")
            
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
            cv2.imshow(f"Entity {entity_id} - Gold Mask", blue_mask)
            cv2.imshow(f"Entity {entity_id} - Blue Mask", red_mask)
            cv2.waitKey(500)  # Wait for 500ms instead of indefinitely
            cv2.destroyAllWindows()

        categorized_entities.append((entity_id, team, round(red_ratio,2), round(blue_ratio,2)))

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
        self.last_card_played = None
        self.elixir_threshold = 6  # Default threshold for playing cards
        self.defense_mode = False
        self.defense_timer = 0
        self.attack_queue = []
        self.last_defense_time = 0
        self.coord_attaque = [[100,370],[335, 370]]
        self.taunt = 0
        self.taunt_compteur = 0
        
        self.start_time = time.time()
        self.start_idle = 2 + self.start_time
        self.last_frame_time = self.start_time
        self.elapsed_time_sinc_last_frame = 0
        self.last_attach_resest = self.start_time
        

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
        #[1, [108, 73], 'destroyed tower', [49, 65], 0-1 vie], [1, [80, 75], 'destroyed tower', [46, 55]], [1, [282, 76], 'destroyed tower', [43, 51]], [0, 'carte 0', 0], [0, 'carte 1', 'geant_vignette.jpg'], [0, 'carte 2', 'geant_vignette.jpg'], [0, 'carte 3', 0], [1, [90, 29], 'fleches', [177, 40]], [1, [334, 367], 'geant', [27, 38]], [1, [349, 350], 'geant', [28, 38]], [1, [328, 360], 'geant', [30, 33]], [1, [334, 339], 'geant', [30, 30]], [1, [351, 322], 'geant', [27, 36]], [1, [338, 312], 'info-message', [31, 41]], [1, [347, 352], 'chevalier', [69, 62]], [1, [369, 342], 'geant', [35, 33]], 
        #[1, [343, 318], 'geant', [39, 46]]]
        self.elapsed_time_sinc_last_frame = time.time() - self.last_frame_time
        self.last_frame_time = time.time()
        print("Elapsed time since last frame:", self.elapsed_time_sinc_last_frame)
        action = []
        
        
        
        # If no state, return empty action
        if not state[0]:
            return []
            
        # Parse game state
        elixir, towers, cards, entities = parse_state(state)
        teams = categorize_teams(entities, image)
        
        # Convert teams list to a dictionary for easier access
        entity_teams = {}
        for i, (entity_id, team, _, _) in enumerate(teams):
            entity_teams[entity_id] = team
        
        # Extract friendly and enemy entities
        friendly_entities = [entities[i] for i, (entity_id, team, _, _) in enumerate(teams) if team == "friendly"]
        enemy_entities = [entities[i] for i, (entity_id, team, _, _) in enumerate(teams) if team == "enemy"]
        
        # Check tower health
        our_towers = [tower for tower in towers if tower[1][1] > 400] # Assume towers under y=400 are ours
        enemy_towers = [tower for tower in towers if tower[1][1] < 400] # Assume towers above y=400 are enemies
        
        #print("our_towers",our_towers)
        #print("enemy_towers",enemy_towers)
        # Bot logic
        if time.time() > self.start_idle and self.taunt == 0 and (enemy_towers[0][2] == "destroyed tower" or enemy_towers[1][2] == "destroyed tower"):
            print("Ennemy tower destroyed, start taunting")
            self.taunt = 1
            self.taunt_compteur = time.time() + 0.5
            return [4, [37,671]]
        elif self.taunt == 1 and time.time() >= self.taunt_compteur:
            self.taunt = 2
            if (enemy_towers[0][2] == "destroyed tower" and enemy_towers[1][2] == "destroyed tower"):
                self.taunt = 3
            return [5, [109,535]]
        elif self.taunt == 2 and (enemy_towers[0][2] == "destroyed tower" and enemy_towers[1][2] == "destroyed tower"):
            self.taunt = 0
            self.taunt_compteur = 0           
        else:
            if time.time() > self.start_idle:
                action = self.decide_action(elixir, our_towers, enemy_towers, cards, friendly_entities, enemy_entities)
        return action

    def decide_action(self, elixir, our_towers, enemy_towers, cards, friendly_entities, enemy_entities):
        # Reset attack queue if needed
        if time.time() - self.last_attach_resest >= 10:  # Every ~10 seconds
            self.attack_queue = []
            self.last_attach_resest = time.time()
        
        # Check if we need to defend
        if self.should_defend(enemy_entities, our_towers) and not self.defense_mode:
            #print("defense")
            self.defense_mode = True
            self.defense_timer = time.time() + 2.5  # Stay in defense mode for ~2.5 seconds
            self.last_defense_time = time.time()
        
        # Check if we can exit defense mode
        if self.defense_mode and time.time() >= self.defense_timer:
            self.defense_mode = False
        elif self.defense_mode:
            print("Remaining in defense mode for {}s".format(self.defense_timer - time.time()))
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
                try:
                    if card_index < len(cards) and elixir >= prix_cartes[cards[card_index][2]]:  # Ensure we have enough elixir
                        self.last_card_played = cards[card_index][1]
                        return [card_index, position]
                except:
                    with open("error_log.txt", "a") as error_file:
                        error_file.write(f"Error with card_index: {card_index}, cards: {cards}\n")
            
            # Otherwise, decide on a new attack
            return self.attack(elixir, enemy_towers, cards, friendly_entities)
        
        # If we have low elixir or just defended, wait
        if elixir < 5 or (time.time() - self.last_defense_time) < 2.5:
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
                defend_x = target_tower[1][0]
                defend_y = target_tower[1][1]-30
                #[78,458,54,65],[312,458,54,65]
                
                self.last_card_played = cards[defender_index][1]
                return [defender_index, [defend_x,defend_y]]
        
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
            defenders_priority = ["PK", "mousquetaire", "chauvesouris", "gargouilles"]  
        elif "mousquetaire" in enemy_type.lower():
            defenders_priority = ["chevalier", "squelettes", "gargouilles", "chauvesouris"]  
        elif "valkyrie" in enemy_type.lower():
            defenders_priority = ["mousquetaire", "PK", "gargouilles", "chauvesouris"]  
        elif "chevalier" in enemy_type.lower():
            defenders_priority = ["mousquetaire", "squelettes", "gobelin_lance", "gargouilles"]  
        elif "PK" in enemy_type.lower():  # Mini P.E.K.K.A
            defenders_priority = ["squelettes", "gobelin_lance", "chauvesouris", "gargouilles"]  
        elif "bat" in enemy_type.lower():
            defenders_priority = ["archere", "gobelin_lance", "mousquetaire"]  
        elif "gargouilles" in enemy_type.lower():
            defenders_priority = ["archere", "gobelin_lance", "mousquetaire"]  
        elif "zappy" in enemy_type.lower():
            defenders_priority = ["PK", "mousquetaire", "squelettes", "gobelin_lance"]  
        elif "gobelin" in enemy_type.lower():
            defenders_priority = ["valkyrie", "chevalier", "squelettes"]  
        elif "gobelin_lance" in enemy_type.lower():
            defenders_priority = ["valkyrie", "chevalier", "archere"]  
        elif "archere" in enemy_type.lower():
            defenders_priority = ["chevalier", "valkyrie", "gargouilles"]  
        elif "squelette" in enemy_type.lower():
            defenders_priority = ["valkyrie", "squelettes", "gobelin_lance"]  
        else:
            # Priorité par défaut
            defenders_priority = ["chevalier", "mousquetaire", "squelettes", "gobelin_lance", "PK"]

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
        #selects the weakest tower, excluding towers that where already destroyed
        if(enemy_towers[0][2]=='destroyed tower'):
            target_tower = enemy_towers[1]
            attack_x,attack_y = self.coord_attaque[1]
        elif(enemy_towers[1][2]=='destroyed tower'):
            target_tower = enemy_towers[0]
            attack_x,attack_y = self.coord_attaque[0]
        elif(enemy_towers[0][4]>enemy_towers[1][4]):
            target_tower = enemy_towers[0]
            attack_x,attack_y = self.coord_attaque[0]
        else:#by default it will atack the right tower
            target_tower = enemy_towers[1]
            attack_x,attack_y = self.coord_attaque[1]
        tower_x, tower_y = target_tower[1][0], target_tower[1][1]
        
        
        # Check for tank cards
        if "geant_vignette.jpg" in card_types:
            tank_index = card_types.index("geant_vignette.jpg")
            self.attack_queue.append([tank_index, [attack_x, attack_y]])
            
            # Queue support troops
            if "archere_vignette.jpg" in card_types:
                support_index = card_types.index("archere_vignette.jpg")
                support_x = attack_x
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
                support_x = attack_x
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
            
            # Queue up split push
            self.attack_queue.append([split_candidates[0], self.coord_attaque[0]])
            self.attack_queue.append([split_candidates[1], self.coord_attaque[1]])
            
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
            if(enemy_towers[0][2]=='destroyed tower'):
                target_tower = enemy_towers[1]
                attack_x,attack_y = self.coord_attaque[1]
            elif(enemy_towers[1][2]=='destroyed tower'):
                target_tower = enemy_towers[0]
                attack_x,attack_y = self.coord_attaque[0]
            elif(enemy_towers[0][4]>enemy_towers[1][4]):
                target_tower = enemy_towers[0]
                attack_x,attack_y = self.coord_attaque[0]
            else:#by default it will atack the right tower
                target_tower = enemy_towers[1]
                attack_x,attack_y = self.coord_attaque[1]
            tower_x, tower_y = target_tower[1][0], target_tower[1][1]
            
            attack_y += 20
            
            # Choose a cheap card
            cheap_card_index = chip_candidates[0]
            
            return [cheap_card_index, [attack_x, attack_y]]
        
        # No good chip cards, wait for better opportunity
        return []
