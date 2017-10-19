# Shadowstone
# Code Angel
# people_items module

import random
import pygame
import os


# Create a dictionary of player characters
def set_up_characters():

    player_a_image = load_image('characters', 'player_a')
    player_b_image = load_image('characters', 'player_b')
    player_c_image = load_image('characters', 'player_c')
    player_d_image = load_image('characters', 'player_d')

    characters = {
        'Player A': {'health': 9,
                     'strength': 5,
                     'dexterity': 8,
                     'magic': 17,
                     'gold': 0,
                     'image': player_a_image},

        'Player B': {'health': 13,
                     'strength': 8,
                     'dexterity': 12,
                     'magic': 13,
                     'gold': 0,
                     'image': player_b_image},

        'Player C': {'health': 14,
                     'strength': 18,
                     'dexterity': 6,
                     'magic': 2,
                     'gold': 0,
                     'image': player_c_image},

        'Player D': {'health': 18,
                     'strength': 12,
                     'dexterity': 17,
                     'magic': 5,
                     'gold': 0,
                     'image': player_d_image},
    }

    return characters


# Create a dictionary of opponent characters
def set_up_opponents():
    shamrassi_image = load_image('characters', 'shamrassi')
    naertho_image = load_image('characters', 'naertho')
    ikarov_image = load_image('characters', 'ikarov')

    opponents = {


        'Shamrassi': {'name': 'Shamrassi',
                      'type': 'sorcerer',
                      'health': 7,
                      'strength': 6,
                      'dexterity': 8,
                      'magic': 19,
                      'gold': 23,
                      'image': shamrassi_image,
                      'level': 1},

        'Naertho': {'name': 'Naertho',
                    'type': 'assassin',
                    'health': 12,
                    'strength': 9,
                    'dexterity': 15,
                    'magic': 4,
                    'gold': 34,
                    'image': naertho_image,
                    'level': 2},

        'Ikarov': {'name': 'Ikarov',
                   'type': 'warrior',
                   'health': 14,
                   'strength': 16,
                   'dexterity': 3,
                   'magic': 1,
                   'gold': 58,
                   'image': ikarov_image,
                   'level': 3},


    }

    return opponents


# Choose one of two random opponents for the current level
def get_next_opponent(opponents, level):

    random_name = random.choice(list(opponents.keys()))
    random_opponent = opponents.get(random_name)
    while random_opponent.get('level') != level:
        random_name = random.choice(list(opponents.keys()))
        random_opponent = opponents.get(random_name)

    return random_opponent


# Create a dictionary of items
def set_up_items():

    empty_item_image = load_image('items', 'empty_item')
    hands_image = load_image('items', 'hands')
    rusted_knife_image = load_image('items', 'rusted_knife')
    huntsman_knife_image = load_image('items', 'huntsman_knife')
    iron_sword_image = load_image('items', 'iron_sword')
    iron_dagger_image = load_image('items', 'iron_dagger')
    steel_dagger_image = load_image('items', 'steel_dagger')
    broken_sword_image = load_image('items', 'broken_sword')
    mace_image = load_image('items', 'mace')
    chain_mace_image = load_image('items', 'chain_mace')
    steel_sword_image = load_image('items', 'steel_sword')
    golden_sword_image = load_image('items', 'golden_sword')

    wooden_shield_image = load_image('items', 'wooden_shield')
    leather_shield_image = load_image('items', 'leather_shield')
    copper_shield_image = load_image('items', 'copper_shield')
    steel_shield_image = load_image('items', 'steel_shield')
    iron_shield_image = load_image('items', 'iron_shield')
    light_steel_shield_image = load_image('items', 'light_steel_shield')

    items = {
        'empty': {'name': 'empty',
                  'type': 'none',
                  'level': 0,
                  'attack': 0,
                  'defence': 0,
                  'magic': 0,
                  'image': empty_item_image},

        'hands': {'name': 'bare hands',
                  'type': 'weapon',
                  'level': 0,
                  'attack': 2,
                  'defence': 0,
                  'magic': 0,
                  'image': hands_image},

        'rusted knife': {'name': 'rusted knife',
                         'type': 'weapon',
                         'level': 1,
                         'attack': 2,
                         'defence': 0,
                         'magic': 0,
                         'image': rusted_knife_image},

        'huntsman knife': {'name': 'huntsman knife',
                           'type': 'weapon',
                           'level': 1,
                           'attack': 4,
                           'defence': 0,
                           'magic': 0,
                           'image': huntsman_knife_image},

        'iron dagger': {'name': 'iron dagger',
                        'type': 'weapon',
                        'level': 1,
                        'attack': 5,
                        'defence': 0,
                        'magic': 0,
                        'image': iron_dagger_image},

        'iron sword': {'name': 'iron sword',
                       'type': 'weapon',
                       'level': 1,
                       'attack': 10,
                       'defence': 0,
                       'magic': 0,
                       'image': iron_sword_image},

        'steel dagger': {'name': 'steel dagger',
                         'type': 'weapon',
                         'level': 2,
                         'attack': 7,
                         'defence': 0,
                         'magic': 0,
                         'image': steel_dagger_image},

        'broken sword': {'name': 'broken sword',
                         'type': 'weapon',
                         'level': 2,
                         'attack': 9,
                         'defence': 0,
                         'magic': 0,
                         'image': broken_sword_image},

        'mace': {'name': 'maceace',
                 'type': 'weapon',
                 'level': 2,
                 'attack': 13,
                 'defence': 0,
                 'magic': 0,
                 'image': mace_image},

        'chain mace': {'name': 'chain mace',
                       'type': 'weapon',
                       'level': 3,
                       'attack': 16,
                       'defence': 0,
                       'magic': 0,
                       'image': chain_mace_image},

        'steel sword': {'name': 'steel sword',
                        'type': 'weapon',
                        'level': 3,
                        'attack': 14,
                        'defence': 0,
                        'magic': 0,
                        'image': steel_sword_image},

        'golden sword': {'name': 'golden sword',
                         'type': 'weapon',
                         'level': 3,
                         'attack': 18,
                         'defence': 0,
                         'magic': 0,
                         'image': golden_sword_image},

        'wooden shield': {'name': 'wooden shield',
                          'type': 'shield',
                          'level': 1,
                          'attack': 0,
                          'defence': 4,
                          'magic': 0,
                          'image': wooden_shield_image},

        'leather shield': {'name': 'leather shield',
                           'type': 'shield',
                           'level': 1,
                           'attack': 0,
                           'defence': 3,
                           'magic': 0,
                           'image': leather_shield_image},

        'copper shield': {'name': 'copper shield',
                          'type': 'shield',
                          'level': 2,
                          'attack': 0,
                          'defence': 6,
                          'magic': 0,
                          'image': copper_shield_image},

        'steel shield': {'name': 'steel shield',
                         'type': 'shield',
                         'level': 2,
                         'attack': 0,
                         'defence': 10,
                         'magic': 0,
                         'image': steel_shield_image},

        'iron shield': {'name': 'iron shield',
                        'type': 'shield',
                        'level': 3,
                        'attack': 0,
                        'defence': 9,
                        'magic': 0,
                        'image': iron_shield_image},

        'light steel shield': {'name': 'light steel shield',
                               'type': 'shield',
                               'level': 3,
                               'attack': 0,
                               'defence': 13,
                               'magic': 0,
                               'image': light_steel_shield_image},

    }

    return items


def get_dice_images():
    dice_1_image = load_image('dice', 'dice_1')
    dice_2_image = load_image('dice', 'dice_2')
    dice_3_image = load_image('dice', 'dice_3')
    dice_4_image = load_image('dice', 'dice_4')
    dice_5_image = load_image('dice', 'dice_5')
    dice_6_image = load_image('dice', 'dice_6')
    dice_7_image = load_image('dice', 'dice_7')
    dice_8_image = load_image('dice', 'dice_8')
    dice_9_image = load_image('dice', 'dice_9')
    dice_10_image = load_image('dice', 'dice_10')
    dice_11_image = load_image('dice', 'dice_11')
    dice_12_image = load_image('dice', 'dice_12')
    dice_13_image = load_image('dice', 'dice_13')
    dice_14_image = load_image('dice', 'dice_14')
    dice_15_image = load_image('dice', 'dice_15')
    dice_16_image = load_image('dice', 'dice_16')
    dice_17_image = load_image('dice', 'dice_17')
    dice_18_image = load_image('dice', 'dice_18')
    dice_19_image = load_image('dice', 'dice_19')
    dice_20_image = load_image('dice', 'dice_20')

    return [dice_1_image, dice_2_image, dice_3_image, dice_4_image, dice_5_image,
            dice_6_image, dice_7_image, dice_8_image, dice_9_image, dice_10_image,
            dice_11_image, dice_12_image, dice_13_image, dice_14_image, dice_15_image,
            dice_16_image, dice_17_image, dice_18_image, dice_19_image, dice_20_image]


# Select an item at random to be won as a reward when the player overcomes an opponent
def win_new_item(level, items):

    item_keys = list(items.keys())

    # Choose a random item
    random_item = random.choice(item_keys)
    random_level = items.get(random_item).get('level')

    # Keep selecting a random item while it is empty or hands
    while random_level > level or random_item == 'empty' or random_item == 'hands':
        random_item = random.choice(item_keys)
        random_level = items.get(random_item).get('level')

    return random_item


# Predefined list of items for the opponent at each level
def get_opponent_items(level):
    opponent_items = ''
    if level == 1:
        opponent_items = ['hands', 'rusted knife', 'empty', 'empty', 'empty', 'wooden shield']
    elif level == 2:
        opponent_items = ['hands', 'huntsman knife', 'steel dagger', 'broken sword', 'empty', 'copper shield']
    elif level == 3:
        opponent_items = ['hands', 'mace', 'steel sword', 'empty', 'empty', 'iron shield']

    return opponent_items


# Predefined list of items for the player at the start of the game
def get_player_items():
    player_items = ['hands', 'steel dagger', 'iron sword', 'empty', 'empty', 'wooden shield']

    return player_items


# Get an image from folder
def load_image(folder_name, filename):
    program_path = os.path.dirname(os.path.realpath(__file__))
    images_path = os.path.join(program_path, 'images')
    folder_path = os.path.join(images_path, folder_name)
    full_path = os.path.join(folder_path, filename + '.png')

    image = pygame.image.load(full_path).convert_alpha()

    return image
