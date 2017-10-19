#!/usr/bin/python
# Shadowstone
# Code Angel

import sys
import os
import pygame
from pygame.locals import *
import random

import people_items

# Define the colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (22, 68, 152)
GREEN = (40, 180, 40)

# Define constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

PRINT_LINE_SIZE = 20
PRINT_BOX_MARGIN = 48

CARD_PADDING = 10
LEFT_MARGIN = 20
CARD_X = 220
DICE_X = 270
DICE_Y = 210
ITEM_X = [406, 482, 555]
CHOOSE_CARD_BOTTOM = 200

TURN_X = 258
PLAYER_TURN_Y = 165
OPPONENT_TURN_Y = 454

PAUSE_TIME = 2000
DICE_ROLL_TIME = 300

STRENGTH_ATTACK_MULTIPLIER = 2
DEXTERITY_ATTACK_MULTIPLIER = 1
WEAPON_ATTACK_MULTIPLIER = 3

STRENGTH_DEFENCE_MULTIPLIER = 0.5
DEXTERITY_DEFENCE_MULTIPLIER = 1
ARMOUR_DEFENCE_MULTIPLIER = 3

# Setup
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shadowstone')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Helvetica', 16)
small_font = pygame.font.SysFont('Helvetica', 10)
large_font = pygame.font.SysFont('Helvetica', 32)

# Load images
background_image = people_items.load_image('general', 'background')
stats_box_image = people_items.load_image('general', 'stats_box')
message_box_image = people_items.load_image('general', 'message_box')
lge_message_box_image = people_items.load_image('general', 'lge_message_box')
player_box_image = people_items.load_image('general', 'player_box')

turn_image = people_items.load_image('general', 'turn')


def main():

    # Initialise variables
    level = 1
    opponent_weapon = ''
    player_weapon = ''

    dice_images = people_items.get_dice_images()

    # Set up player opponents and items dictionary
    opponents = people_items.set_up_opponents()
    characters = people_items.set_up_characters()

    # items = people.set_up_items(item_images)
    items = people_items.set_up_items()

    # Set up items
    player_items = people_items.get_player_items()

    game_screen.blit(background_image, [0, 0])
    display_choose_characters(characters)
    pygame.display.update()

    player_character = ''
    character_chosen = False

    # repeat until character 1-4 chosen
    while character_chosen is False:

        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()

            if key_pressed[pygame.K_1]:
                player_character = characters.get('Player A')
                character_chosen = True

            elif key_pressed[pygame.K_2]:
                player_character = characters.get('Player B')
                character_chosen = True

            elif key_pressed[pygame.K_3]:
                player_character = characters.get('Player C')
                character_chosen = True

            elif key_pressed[pygame.K_4]:
                player_character = characters.get('Player D')
                character_chosen = True

            check_for_quit(event)

    # 3 Conquests as long as player has health
    player_health = player_character.get('health')

    while player_health > 0 and level < 4:

        # Display the scene description and wait for RETURN to be pressed
        opponent = people_items.get_next_opponent(opponents, level)
        opponent_items = people_items.get_opponent_items(level)

        game_screen.blit(background_image, [0, 0])
        display_description(level, opponent.get('name'), opponent.get('type'))
        pygame.display.update()

        wait_for_return()

        # Display board
        game_screen.blit(background_image, [0, 0])
        display_board(opponent, player_character, opponent_items, player_items, items)

        opponent_name = opponent.get('name')
        board_message_box('You come face to face with ' + opponent_name + '.')
        
        pygame.display.update()
        wait_for_return()

        # Play Turn
        turn = random.choice(['Player', 'Opponent'])

        opponent_health = opponent.get('health')

        # Keep playing while both still have health
        while opponent_health > 0 and player_health > 0:

            if turn == 'Opponent':
                board_message_box(opponent_name + ' strikes...')
                game_screen.blit(turn_image, [TURN_X, OPPONENT_TURN_Y])
            else:
                board_message_box('You attack ' + opponent_name + '...')
                game_screen.blit(turn_image, [TURN_X, PLAYER_TURN_Y])

            pygame.display.update()
            wait_for_return()

            # Opponent attack
            if turn == 'Opponent':
                
                opponent_weapon = get_opponent_weapon(opponent_items, items)
                player_shield = get_specific_item(player_items, items, 'Shield')
                attack_dice = get_attack_dice(opponent, opponent_weapon, player_character, player_shield)

                board_message_box(opponent.get('name') +
                                  ' attacks you with a ' +
                                  opponent_weapon.get('name') +
                                  ', needs to roll a '
                                  + str(attack_dice) +
                                  ' or above.')

            else:

                # Player attack
                board_message_box('Choose a weapon to attack (1-5)')
                pygame.display.update()

                # Get a valid weapon number (1-5)
                weapon_no = 0

                while weapon_no == 0:
                    for event in pygame.event.get():
                        key_pressed = pygame.key.get_pressed()

                        if key_pressed[pygame.K_1]:
                            weapon_no = 1
                        elif key_pressed[pygame.K_2]:
                            weapon_no = 2
                        elif key_pressed[pygame.K_3]:
                            weapon_no = 3
                        elif key_pressed[pygame.K_4]:
                            weapon_no = 4
                        elif key_pressed[pygame.K_5]:
                            weapon_no = 5

                        if weapon_no > 0:
                            if player_items[weapon_no - 1] == 'empty':
                                weapon_no = 0
                                board_message_box('No weapon in that slot. Choose a weapon to attack (1-5)')
                                pygame.display.update()

                        check_for_quit(event)

                player_weapon_chosen = player_items[weapon_no - 1]
                player_weapon = items.get(player_weapon_chosen)
                opponent_shield = get_specific_item(opponent_items, items, 'Shield')

                attack_dice = get_attack_dice(player_character, player_weapon, opponent, opponent_shield)

                board_message_box('You attack with a ' +
                                  player_weapon.get('name') +
                                  ' and need to roll a ' +
                                  str(attack_dice) +
                                  ' or above.')

            pygame.display.update()
            wait_for_return()

            # Roll Attack Chance
            board_message_box('')

            chance_roll = random.randint(1, 20)
            game_screen.blit(dice_images[chance_roll - 1], [DICE_X, DICE_Y])
            pygame.display.update()
            wait_for_return()

            # Attack is successful
            if chance_roll >= attack_dice:
                board_message_box('Attack succeeded, rolling for health damage...')
                pygame.display.update()
                wait_for_return()

                if turn == 'Opponent':
                    max_damage = opponent_weapon.get('attack')
                else:
                    max_damage = player_weapon.get('attack')

                board_message_box('')

                # Roll for damage
                damage_roll = random.randint(1, max_damage)
                game_screen.blit(dice_images[damage_roll - 1], [DICE_X, DICE_Y])
                
                pygame.display.update()
                wait_for_return()

                # Reduce health points
                if turn == 'Opponent':
                    player_health -= damage_roll
                    player_character['health'] = player_health
                    board_message_box('Your health takes a damage of ' + str(damage_roll) + '.')

                else:
                    opponent_health -= damage_roll
                    opponent['health'] = opponent_health
                    board_message_box(opponent_name + ' takes a damage of ' + str(damage_roll) + ' to health.')

                pygame.display.update()
                wait_for_return()

                # If both players still alive, random test for weapon or armour damage
                if opponent_health > 0 and player_health > 0:

                    board_message_box('Checking for any weapon or armour damage...')
                    pygame.display.update()
                    wait_for_return()

                    if turn == 'Opponent':
                        damage_item = random.choice(player_items)
                    else:
                        damage_item = random.choice(opponent_items)

                    if damage_item == 'hands' or damage_item == 'empty':

                        # If empty slot or hands slot selected, no damage
                        board_message_box('No weapon or armour damage inflicted.')
                        pygame.display.update()
                        wait_for_return()

                    else:

                        # Item is damaged so remove it
                        damage_item_name = items.get(damage_item).get('name')
                        board_message_box(damage_item_name + ' is destroyed!')

                        if turn == 'Opponent':
                            position = player_items.index(damage_item)
                            player_items[position] = 'empty'
                        else:
                            position = opponent_items.index(damage_item)
                            opponent_items[position] = 'empty'

                        pygame.display.update()
                        wait_for_return()

            else:

                # Attack has failed
                board_message_box('Attack failed!')

                pygame.display.update()
                wait_for_return()

            # Is player or opponent health 0 or less?
            if player_health <= 0:
                board_message_box('You have been defeated by ' + opponent.get('name') + '!!!')
            elif opponent_health <= 0:

                # Boost player health with random value
                health_boost = random.randint(1, 3) * level

                board_message_box('You have defeated ' +
                                  opponent.get('name') +
                                  '. Your health is boosted by ' +
                                  str(health_boost) + '.')

                player_character['health'] = player_health + health_boost

                pygame.display.update()
                wait_for_return()

                # Give player any gold the opponent had
                gold = opponent.get('gold')
                player_character['gold'] = player_character.get('gold') + gold

                reward_item = people_items.win_new_item(level, items)
                reward_item_name = items.get(reward_item).get('name')
                reward_item_type = items.get(reward_item).get('type')

                board_message_box('You have won ' +
                                  str(gold) +
                                  ' gold pieces and also receive a ' +
                                  reward_item_name + '.')

                # If reward is a shield, replace existing shield
                if reward_item_type == 'shield':
                    player_items[len(player_items) - 1] = reward_item
                else:

                    # If reward is not a shield, find first empty slot
                    for item_counter, inventory_item in enumerate(player_items):
                        if inventory_item == 'empty':
                            player_items[item_counter] = reward_item
                            break

                pygame.display.update()
                wait_for_return()

                level += 1

            else:
                # Reverse turns
                if turn == 'Opponent':
                    turn = 'Player'
                else:
                    turn = 'Opponent'

            game_screen.blit(background_image, [0, 0])
            display_board(opponent, player_character, opponent_items, player_items, items)
            board_message_box('')
            pygame.display.update()

    # End of Game
    game_screen.blit(background_image, [0, 0])

    if player_health > 0:
        final_gold = player_character.get('gold')
        overlay_message(['In battle you are victorious.'
                         'You have been crowned the Champion of Shadowstone.',
                         '',
                         'You have earned ' + str(final_gold) + ' gold pieces as your reward.'])
    else:
        overlay_message(['Like many who came before, you have fallen in the ancient city of Shadowstone.',
                         '',
                         'There will be many others who foolishly follow in your steps.'])

    pygame.display.update()
    wait_for_return()


# Check if the user has tried to quit
def check_for_quit(event):
    if event.type == QUIT:
        pygame.quit()
        sys.exit()


# Wait until return key is pressed
def wait_for_return():

    return_pressed = False
    while return_pressed is False:

        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()

            if key_pressed[pygame.K_RETURN]:
                return_pressed = True

            check_for_quit(event)


# Display the 4 possible player characters
def display_choose_characters(characters):

    message_box_y = 360

    # set up cards and names
    player_a_card_image = characters.get('Player A').get('image')
    player_b_card_image = characters.get('Player B').get('image')
    player_c_card_image = characters.get('Player C').get('image')
    player_d_card_image = characters.get('Player D').get('image')

    char_card_width = get_image_width(player_a_card_image)

    # display cards
    spacing = (SCREEN_WIDTH - char_card_width * 4) / 5
    col_1_x = spacing
    col_2_x = char_card_width + 2 * spacing
    col_3_x = 2 * char_card_width + 3 * spacing
    col_4_x = 3 * char_card_width + 4 * spacing

    player_a_y = CHOOSE_CARD_BOTTOM - get_image_height(player_a_card_image)
    player_b_y = CHOOSE_CARD_BOTTOM - get_image_height(player_b_card_image)
    player_c_y = CHOOSE_CARD_BOTTOM - get_image_height(player_c_card_image)
    player_d_y = CHOOSE_CARD_BOTTOM - get_image_height(player_d_card_image)
    game_screen.blit(player_a_card_image, [col_1_x, player_a_y])
    game_screen.blit(player_b_card_image, [col_2_x, player_b_y])
    game_screen.blit(player_c_card_image, [col_3_x, player_c_y])
    game_screen.blit(player_d_card_image, [col_4_x, player_d_y])

    # Boxes underneath with numbers
    player_box_y = CHOOSE_CARD_BOTTOM + CARD_PADDING
    player_box_text_y = CHOOSE_CARD_BOTTOM + CARD_PADDING + 5

    game_screen.blit(player_box_image, [col_1_x, player_box_y])
    game_screen.blit(player_box_image, [col_2_x, player_box_y])
    game_screen.blit(player_box_image, [col_3_x, player_box_y])
    game_screen.blit(player_box_image, [col_4_x, player_box_y])

    # Display the numbers
    centre_text_with_object('Press 1', col_1_x, char_card_width, player_box_text_y, BLACK)
    centre_text_with_object('Press 2', col_2_x, char_card_width, player_box_text_y, BLACK)
    centre_text_with_object('Press 3', col_3_x, char_card_width, player_box_text_y, BLACK)
    centre_text_with_object('Press 4', col_4_x, char_card_width, player_box_text_y, BLACK)

    # Main message box
    message = 'Choose your character (1-4)'
    message_box_width = SCREEN_WIDTH - 2 * LEFT_MARGIN
    game_screen.blit(message_box_image, [LEFT_MARGIN, message_box_y])
    centre_text_with_object(message, LEFT_MARGIN, message_box_width, message_box_y + 28, BLACK)


# Centre any piece of text with a given object
def centre_text_with_object(display_text, object_x, object_width, text_y_coord, text_color):

    text = font.render(display_text, True, text_color)
    text_rect = text.get_rect()
    text_x_coord = object_x + (object_width - text_rect.width) / 2

    game_screen.blit(text, [text_x_coord, text_y_coord])


# Display a level description
def display_description(level, next_opponent_name, next_opponent_type):

    all_levels = [['You arrive at the Kings Tavern, an old inn at the edge of the city. After a light ',
                   'refreshment, you notice a shadow from behind and when turning around you are ',
                   'met by '],

                  ['You walk out into the town square. The low sun casts shadows all around as ',
                   'you edge your way towards the old cathedral at the far end of the square. As your',
                   'eyes adjust you notice a figure moving in a doorway. It is '],

                  ['The doors to the old cathedral swing open. Slowly you edge your way through the  ',
                   'town square to the entrance. It is cold and gloomy inside but through the darkness ',
                   'you just make out someone waiting in the far corner. It is '],
                  ]

    level_text = all_levels[level - 1]
    last_line = len(level_text) - 1
    level_text[last_line] += next_opponent_name + ', the ' + next_opponent_type + '.'
    overlay_message(level_text)


# Display a message on screen taking in a list of lines of text to be displayed
def overlay_message(text_to_display):

    box_top = 180
    box_left = 50

    game_screen.blit(lge_message_box_image, [box_left, box_top])

    number_of_lines = len(text_to_display)

    for line_number, line in enumerate(text_to_display):
        display_line = font.render(line, True, BLACK)

        message_loc = [PRINT_BOX_MARGIN + PRINT_LINE_SIZE, box_top + PRINT_LINE_SIZE + line_number * PRINT_LINE_SIZE]
        game_screen.blit(display_line, message_loc)

    # Add a final line of text to tell the user to hit RETURN
    final_line = font.render('[Hit RETURN to continue]', True, BLACK)
    final_line_rect = final_line.get_rect()
    final_line_loc = [(SCREEN_WIDTH - final_line_rect.width) / 2,
                      box_top + 2 * PRINT_LINE_SIZE + number_of_lines * PRINT_LINE_SIZE]

    game_screen.blit(final_line, final_line_loc)


# Display a centred message across the middle band of the board
def board_message_box(message):
    message_box_width = SCREEN_WIDTH - 2 * LEFT_MARGIN
    game_screen.blit(message_box_image, [LEFT_MARGIN, SCREEN_HEIGHT / 2 - 2 * PRINT_LINE_SIZE])
    centre_text_with_object(message, LEFT_MARGIN, message_box_width, (SCREEN_HEIGHT - PRINT_LINE_SIZE) / 2, BLACK)


# Display the main board
def display_board(opponent, player, opponent_items, player_items, items):
    player_card_image = player.get('image')
    opponent_card_image = opponent.get('image')
    empty_item_image = items.get('empty').get('image')
    item_width = get_image_width(empty_item_image)
    item_height = get_image_height(empty_item_image)

    # display opponent
    opponent_card_y = 292
    game_screen.blit(opponent_card_image, [CARD_X, opponent_card_y])

    # display player
    player_card_y = CARD_PADDING
    game_screen.blit(player_card_image, [CARD_X, player_card_y])

    # Draw display boxes
    box_left = LEFT_MARGIN

    game_screen.blit(stats_box_image, [box_left, opponent_card_y])
    game_screen.blit(stats_box_image, [box_left, player_card_y])

    # Display stats
    opponent_name = opponent.get('name')
    display_stats(opponent_name, opponent_card_y, 0)

    opponent_hea_text = 'Health: ' + str(opponent.get('health'))
    display_stats(opponent_hea_text, opponent_card_y, 2)

    opponent_str_text = 'Strength: ' + str(opponent.get('strength'))
    display_stats(opponent_str_text, opponent_card_y, 3)

    opponent_dex_text = 'Dexterity: ' + str(opponent.get('dexterity'))
    display_stats(opponent_dex_text, opponent_card_y, 4)

    opponent_mag_text = 'Magic: ' + str(opponent.get('magic'))
    display_stats(opponent_mag_text, opponent_card_y, 5)

    opponent_gold_text = 'Gold: ' + str(opponent.get('gold'))
    display_stats(opponent_gold_text, opponent_card_y, 6)

    display_stats('You', player_card_y, 0)

    player_hea_text = 'Health: ' + str(player.get('health'))
    display_stats(player_hea_text, player_card_y, 2)

    player_str_text = 'Strength: ' + str(player.get('strength'))
    display_stats(player_str_text, player_card_y, 3)

    player_dex_text = 'Dexterity: ' + str(player.get('dexterity'))
    display_stats(player_dex_text, player_card_y, 4)

    player_mag_text = 'Magic: ' + str(player.get('magic'))
    display_stats(player_mag_text, player_card_y, 5)

    player_gold_text = 'Gold: ' + str(player.get('gold'))
    display_stats(player_gold_text, player_card_y, 6)

    # Display player items
    for item_no, player_item in enumerate(player_items):
        item = items.get(player_item)
        item_image = item.get('image')
        item_type = item.get('type')

        item_value = 0
        if item_type == 'weapon':
            item_value = item.get('attack')
        elif item_type == 'shield' or item_type == 'armour':
            item_value = item.get('defence')

        # If item_no is 0 - 2 then display on first line
        if item_no < 3:
            item_x = ITEM_X[item_no]
            item_y = player_card_y

        # If item no is 3 - 5 then display on second line
        else:
            item_x = ITEM_X[item_no - 3]
            item_y = player_card_y + item_height + PRINT_LINE_SIZE

        game_screen.blit(item_image, [item_x, item_y])

        # Display the attack / defence value of the item if it has one
        if item_value > 0:
            display_item_value(item_x + item_width, item_y + item_height, item_value)

        # If item_no is between 0 & 4 it's a weapon so display the item number (+1 to make it 1-5)
        if item_no < 5:
            centre_text_with_object(str(item_no + 1), item_x, item_width, item_y + item_height, BLACK)

    # Display opponent items
    for opponent_item_no, opponent_item in enumerate(opponent_items):
        opp_item = items.get(opponent_item)
        opp_item_image = opp_item.get('image')
        opp_item_type = opp_item.get('type')

        opp_item_value = 0
        if opp_item_type == 'weapon':
            opp_item_value = opp_item.get('attack')
        elif opp_item_type == 'shield' or opp_item_type == 'armour':
            opp_item_value = opp_item.get('defence')

        # If item_no is 0 - 2 then display on first line
        if opponent_item_no < 3:
            item_x = ITEM_X[opponent_item_no]
            item_y = opponent_card_y

        # If item no is 3 - 5 then display on second line
        else:
            item_x = ITEM_X[opponent_item_no - 3]
            item_y = opponent_card_y + item_height + PRINT_LINE_SIZE

        game_screen.blit(opp_item_image, [item_x, item_y])

        # Display the attack / defence value of the item if it has one
        if opp_item_value > 0:
            display_item_value(item_x + item_width, item_y + item_height, opp_item_value)


# Select a random weapon for the opponent to attack with
def get_opponent_weapon(opponent_items, items):

    # Select a random item from the opponent's list of items
    random_item_name = random.choice(opponent_items)
    random_item = items.get(random_item_name)
    random_item_type = random_item.get('type')

    # Make sure it is a weapon, if not keep selecting another random item until a weapon is chosen
    while random_item_type != 'weapon':
        random_item_name = random.choice(opponent_items)
        random_item = items.get(random_item_name)
        random_item_type = random_item.get('type')

    return random_item


# Get a specific item type e.g. weapon, shield etc
def get_specific_item(character_items, all_items, search_item_type):

    specific_item = 'Not found'
    for item_name in character_items:
        item = all_items.get(item_name)
        item_type = item.get('type')
        if item_type == search_item_type:
            specific_item = item

    return specific_item


# Work out the number on the dice that needs to be rolled if the attack is to be successful
def get_attack_dice(attacker, attack_weapon, defender, defence_shield):

    # Calculate an attack score
    # Max is 120
    # Divide by 6 to get an attack score out of 20
    attacker_strength = attacker.get('strength')
    attacker_dexterity = attacker.get('dexterity')
    attacker_weapon_attack = attack_weapon.get('attack')

    attack_score = (attacker_strength * STRENGTH_ATTACK_MULTIPLIER +
                    attacker_dexterity * DEXTERITY_ATTACK_MULTIPLIER +
                    attacker_weapon_attack * WEAPON_ATTACK_MULTIPLIER)

    attack_score = int(attack_score / 6)

    # Calculate a defence score
    # Max is 90
    # Divide by 6 to get a defence score out of 15
    defender_strength = defender.get('strength')
    defender_dexterity = defender.get('dexterity')

    if defence_shield == 'Not found':
        armour_defence = 0
    else:
        armour_defence = defence_shield.get('defence')

    defence_score = (defender_strength * STRENGTH_DEFENCE_MULTIPLIER +
                     defender_dexterity * DEXTERITY_DEFENCE_MULTIPLIER +
                     armour_defence * ARMOUR_DEFENCE_MULTIPLIER)

    defence_score = int(defence_score / 6)

    # If attack and defence are the same, looking to roll a 10 or more
    # If attack is much stronger than defence, then a lower (than 10) score required
    # If defence is much stronger than attack, then a higher (than 10) score required
    dice_score = 10 - int((attack_score - defence_score) / 2)
    if dice_score > 20:
        dice_score = 20
    elif dice_score < 1:
        dice_score = 1

    return dice_score


# Format the display of the board game stats, aligned with the relevant card (horizontally)
def display_stats(display_text, box_top, line_no):
    text_x_coord = LEFT_MARGIN + CARD_PADDING
    text_y_coord = box_top + 2 * CARD_PADDING + PRINT_LINE_SIZE * line_no

    text = font.render(display_text, True, BLACK)
    game_screen.blit(text, [text_x_coord, text_y_coord])


# Display the item attack / defence value in the bottom right of each item box
def display_item_value(item_box_right, item_box_bottom, item_score):
    box_size = 14

    # Draw a box
    item_score_rect = (item_box_right - box_size, item_box_bottom - box_size, box_size, box_size)
    pygame.draw.rect(game_screen, GREEN, item_score_rect)

    # Display the text, centred in the box
    text = small_font.render(str(item_score), True, WHITE)
    text_rect = text.get_rect()
    text_width = text_rect.width
    text_height = text_rect.height

    text_x_coord = item_box_right - (box_size + text_width) / 2
    text_y_coord = item_box_bottom - (box_size + text_height) / 2

    game_screen.blit(text, [text_x_coord, text_y_coord])
    

# Calculate the width of an image
def get_image_width(image):
    image_width = image.get_rect().width
    return image_width


# Calculate the height of an image
def get_image_height(image):
    image_height = image.get_rect().height
    return image_height


if __name__ == '__main__':
    main()
