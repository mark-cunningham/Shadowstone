import random
import pygame

# Create a dictionary of player characters
def set_up_characters():
    player_a_image = pygame.image.load("player_a.png").convert()
    player_b_image = pygame.image.load("player_b.png").convert()
    player_c_image = pygame.image.load("player_c.png").convert()
    player_d_image = pygame.image.load("player_d.png").convert()

    characters = {
        'Player A': {'name': 'Player A', 'health': 10, 'strength': 11, 'dexterity': 12, 'magic': 13, 'gold': 0,
                        'image': player_a_image},
        'Player B': {'name': 'Player B', 'health': 20, 'strength': 20, 'dexterity': 20, 'magic': 20, 'gold': 0,
                        'image': player_b_image},
        'Player C': {'name': 'Player C', 'health': 20, 'strength': 20, 'dexterity': 20, 'magic': 20, 'gold': 0,
                        'image': player_c_image},
        'Player D': {'name': 'Player D', 'health': 20, 'strength': 20, 'dexterity': 20, 'magic': 20, 'gold': 0,
                        'image': player_d_image},
    }

    return characters


# Create a dictionary of opponent characters
def set_up_opponents():
    ikarov_image = pygame.image.load("ikarov.png").convert()
    shamrassi_image = pygame.image.load("shamrassi.png").convert()

    opponents = {
        'Ikarov': {'name': 'Ikarov', 'health': 5, 'strength': 16, 'dexterity': 2, 'magic': 1, 'gold': 22,
                   'image': ikarov_image, 'level': 1},
        'Shamrassi': {'name': 'Shamrassi', 'health': 5, 'strength': 13, 'dexterity': 5, 'magic': 2, 'gold': 23,
                      'image': shamrassi_image, 'level': 1},
        'Naertho': {'name': 'Naertho', 'health': 6, 'strength': 13, 'dexterity': 5, 'magic': 2, 'gold': 34,
                      'image': shamrassi_image, 'level': 2},
        'Luvon': {'name': 'Luvon', 'health': 6, 'strength': 13, 'dexterity': 5, 'magic': 2, 'gold': 36,
                      'image': shamrassi_image, 'level': 2},
        'Cloikalk': {'name': 'Cloikalk', 'health': 8, 'strength': 13, 'dexterity': 5, 'magic': 2, 'gold': 51,
                    'image': shamrassi_image, 'level': 3},
        'Vrageekt': {'name': 'Vrageekt', 'health': 8, 'strength': 13, 'dexterity': 5, 'magic': 2, 'gold': 54,
                  'image': shamrassi_image, 'level': 3}
    }

    return opponents

# Choose one of two random opponents for the current level
def get_next_opponent(opponents, level):

    random_name = random.choice(list(opponents.keys()))
    random_opponent = opponents.get(random_name)
    while random_opponent.get('level') != level:
        random_name = random.choice(list(opponents.keys()))
        random_opponent = opponents.get(random_name)

    #next_opponent_number = random.randint(level * 2 - 2, level * 2 - 1)
    #next_opponent_name = opponent_names[next_opponent_number]

    return random_opponent

# Create a dictionary of items
def set_up_items():
    empty_item_image = pygame.image.load("item_empty.png").convert()
    hands_image = pygame.image.load("item_hands.png").convert()
    knife_1_image = pygame.image.load("item_knife_1.png").convert()
    sword_1_image = pygame.image.load("item_sword_1.png").convert()
    shield_1_image = pygame.image.load("item_shield_1.png").convert()
    shield_2_image = pygame.image.load("item_shield_2.png").convert()
    items = {
        'Empty': {'name': 'Empty', 'type': 'None', 'level': 0, 'attack': 0, 'defence': 0, 'magic': 0,
                  'image': empty_item_image},
        'Hands': {'name': 'Bare Hands', 'type': 'Weapon', 'level': 0, 'attack': 2, 'defence': 0, 'magic': 0,
                  'image': hands_image},
        'Knife 1': {'name': 'Rusted Knife', 'type': 'Weapon', 'level': 1, 'attack': 2, 'defence': 0, 'magic': 0,
                    'image': knife_1_image},
        'Knife 2': {'name': 'Sharp Knife', 'type': 'Weapon', 'level': 1, 'attack': 4, 'defence': 0, 'magic': 0,
                    'image': knife_1_image},
        'Sword 1': {'name': 'Bronze Sword', 'type': 'Weapon', 'level': 1, 'attack': 14, 'defence': 0, 'magic': 0,
                    'image': sword_1_image},
        'Sword 2': {'name': 'Iron Sword', 'type': 'Weapon', 'level': 2, 'attack': 8, 'defence': 0, 'magic': 0,
                    'image': sword_1_image},
        'Sword 3': {'name': 'Steel Sword', 'type': 'Weapon', 'level': 3, 'attack': 10, 'defence': 0, 'magic': 0,
                    'image': sword_1_image},
        'Mace 1': {'name': 'Stone Mace', 'type': 'Weapon', 'level': 2, 'attack': 10, 'defence': 0, 'magic': 0,
                    'image': sword_1_image},
        'Mace 2': {'name': 'Chain Mace', 'type': 'Weapon', 'level': 2, 'attack': 12, 'defence': 0, 'magic': 0,
                    'image': sword_1_image},
        'Mace 3': {'name': 'No Mercy Mace', 'type': 'Weapon', 'level': 3, 'attack': 16, 'defence': 0, 'magic': 0,
                    'image': sword_1_image},
        'Shield 1': {'name': 'Wooden Shield', 'type': 'Shield', 'level': 1, 'attack': 0, 'defence': 2, 'magic': 0,
                     'image': shield_1_image},
        'Shield 2': {'name': 'Iron Shield', 'type': 'Shield', 'level': 2, 'attack': 0, 'defence': 6, 'magic': 0,
                     'image': shield_2_image}
    }

    return items

# Select an item at random to be won as a reward when the player overcomes an opponent
def win_new_item(level, items):

    item_keys = list(items.keys())

    # Choose a random item
    random_item = random.choice(item_keys)
    random_level = items.get(random_item).get('level')

    # Keep selecting a random item while it is empty or hands
    while random_level > level or random_item == 'Empty' or random_item == 'Hands':
        random_item = random.choice(item_keys)
        random_level = items.get(random_item).get('level')

    return random_item

# Predefined list of items for the opponent at each level
def get_opponent_items(level):
    opponent_items = ""
    if level == 1:
        opponent_items = ['Hands', 'Knife 1', 'Empty', 'Empty', 'Empty', 'Shield 1']
    elif level == 2:
        opponent_items = ['Hands', 'Knife 1', 'Empty', 'Empty', 'Empty', 'Shield 2']
    elif level == 3:
        opponent_items = ['Hands', 'Knife 1', 'Empty', 'Empty', 'Empty', 'Shield 2']

    return opponent_items


# Predefined list of items for the player at the start of the game
def get_player_items():
    player_items = ['Hands', 'Sword 1', 'Empty', 'Empty', 'Empty', 'Shield 1']

    return player_items