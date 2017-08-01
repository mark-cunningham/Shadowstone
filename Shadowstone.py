# Shadowstone

import sys
import os
import pygame
from pygame.locals import *
import random

import people

# Define the colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKBLUE = (22, 68, 152)
BIEGE = (213, 207, 194)
GREY = (150, 150, 150)
RED =  (183, 40, 40)
GREEN =  (40, 180, 40)
BLUE = (40, 40, 180)

# Define constants
SCREENWIDTH = 640
SCREENHEIGHT = 480

PRINTLINESIZE = 20
PRINTBOXMARGIN = 48

CARDPADDING = 10
LEFTMARGIN = 20
CARD_X = 220
DICE_X = 270
DICE_Y = 210
ITEM_X = [406, 482, 555]

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
game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Shadowstone")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Helvetica", 16)
small_font = pygame.font.SysFont("Helvetica", 10)
large_font = pygame.font.SysFont("Helvetica", 32)

# Load images
background_image = pygame.image.load("background.png").convert()
stats_box_image = pygame.image.load("stats_box.png").convert()
message_box_image = pygame.image.load("message_box.png").convert()

up_arrow_image = pygame.image.load("up_arrow.png").convert()
down_arrow_image = pygame.image.load("down_arrow.png").convert()
turn_image = pygame.image.load("turn.png").convert()
dice_1_image = pygame.image.load("dice_1.png").convert()
dice_15_image = pygame.image.load("dice_15.png").convert()


def main():

    # Initialise variables
    level = 1
    opponent_weapon = ''
    player_weapon = ''
    event = ''

    dice_images = [dice_1_image, dice_15_image, dice_15_image, dice_15_image, dice_15_image, dice_15_image,
                   dice_15_image, dice_15_image, dice_15_image, dice_15_image, dice_15_image, dice_15_image,
                   dice_15_image, dice_15_image, dice_15_image, dice_15_image, dice_15_image, dice_15_image,
                   dice_15_image, dice_15_image]

    # Set up player opponents and items dictionary
    opponents = people.set_up_opponents()
    characters = people.set_up_characters()

    # items = people.set_up_items(item_images)
    items = people.set_up_items()

    # Set up items
    player_items = people.get_player_items()


    player_character = ''

    game_screen.blit(background_image, [0, 0])
    display_choose_characters(characters)
    pygame.display.update()

    while player_character == '':

        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()

            if key_pressed[pygame.K_1]:
                player_character = characters.get('Player A')
            elif key_pressed[pygame.K_2]:
                player_character = characters.get('Player B')
            elif key_pressed[pygame.K_3]:
                player_character = characters.get('Player C')
            elif key_pressed[pygame.K_4]:
                player_character = characters.get('Player D')

        check_for_quit(event)

    # 3 Conquests as long as player has health

    player_health = player_character.get('health')

    while player_health > 0 and level < 4:

        # Display the scene description and wait for RETURN to be pressed
        #opponent_name = people.get_next_opponent(opponent_names, level)
        #opponent = opponents.get(opponent_name)
        opponent = people.get_next_opponent(opponents, level)
        opponent_items = people.get_opponent_items(level)

        game_screen.blit(background_image, [0, 0])
        display_description(level, opponent.get('name'))
        pygame.display.update()

        return_pressed = False

        while return_pressed is False:

            for event in pygame.event.get():
                key_pressed = pygame.key.get_pressed()

                if key_pressed[pygame.K_RETURN]:
                    return_pressed = True

            check_for_quit(event)


        # Work out who Starts

        return_pressed = False

        game_screen.blit(background_image, [0, 0])
        display_board(opponent, player_character, opponent_items, player_items, items)
        board_message_box('Hit RETURN to see who starts')
        pygame.display.update()

        while return_pressed is False:
            for event in pygame.event.get():
                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_RETURN]:
                    return_pressed = True

            check_for_quit(event)

        board_message_box('')
        pygame.display.update()
        pygame.time.wait(PAUSE_TIME)


        # Play Turn
        turn = random.choice(['Player', 'Opponent'])

        opponent_health = opponent.get('health')

        while opponent_health > 0 and player_health > 0:  # Keep playing while both still have health

            # Display the turn arrow
            if turn == 'Opponent':
                display_arrow = down_arrow_image
            else:
                display_arrow = up_arrow_image

            arrow_rect = display_arrow.get_rect()
            arrow_rect.centerx = SCREENWIDTH / 2
            arrow_rect.centery = SCREENHEIGHT / 2

            game_screen.blit(display_arrow, arrow_rect)


            if turn == 'Player':
                game_screen.blit(turn_image, [TURN_X, PLAYER_TURN_Y])
            else:
                game_screen.blit(turn_image, [TURN_X, OPPONENT_TURN_Y])


            pygame.display.update()
            pygame.time.wait(PAUSE_TIME)



            if turn == 'Opponent':

                # Opponent attack
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
                            if player_items[weapon_no - 1] == 'Empty':
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
            pygame.time.wait(PAUSE_TIME)


            # Roll Attack Chance
            board_message_box('')
            chance_roll = 0

            # Keep dice rolling a few times
            spins = random.randint(5, 8)
            for spin in range(spins):
                chance_roll = random.randint(1, 20)
                game_screen.blit(dice_images[chance_roll - 1], [DICE_X, DICE_Y])
                #display_dice(chance_roll, RED)

                pygame.display.update()
                pygame.time.wait(DICE_ROLL_TIME)

            pygame.time.wait(PAUSE_TIME)

            # Attack is successful
            if chance_roll >= attack_dice:
                board_message_box('Attack succeeded, now rolling for health damage...')
                pygame.display.update()
                pygame.time.wait(PAUSE_TIME)

                if turn == 'Opponent':
                    max_damage = opponent_weapon.get('attack')
                else:
                    max_damage = player_weapon.get('attack')

                board_message_box('')

                # Roll the dice for damage hits
                spins = random.randint(5, 8)
                damage_roll = 0

                for spin in range(spins):
                    damage_roll = random.randint(1, max_damage)
                    game_screen.blit(dice_images[damage_roll - 1], [DICE_X, DICE_Y])
                    #display_dice(damage_roll, BLUE)

                    pygame.display.update()
                    pygame.time.wait(DICE_ROLL_TIME)

                pygame.time.wait(PAUSE_TIME)

                # Reduce health points
                if turn == 'Opponent':
                    player_health -= damage_roll
                    player_character['health'] = player_health
                    board_message_box('Your health takes a damage of ' + str(damage_roll) + '.')

                else:
                    opponent_health -= damage_roll
                    opponent['health'] = opponent_health
                    board_message_box(opponent.get('name') + ' takes a damage of ' + str(damage_roll) + ' to health.')

                pygame.display.update()
                pygame.time.wait(PAUSE_TIME)

                # If both players still alive, random test for weapon or armour damage
                if opponent_health > 0 and player_health > 0:

                    board_message_box('Finally, rolling for any weapon or armour damage...')
                    pygame.display.update()
                    pygame.time.wait(PAUSE_TIME)

                    if turn == 'Opponent':
                        damage_item = random.choice(player_items)
                    else:
                        damage_item = random.choice(opponent_items)


                    if damage_item == 'Hands' or damage_item == 'Empty':

                        # If empty slot or hands slot selected, no damage
                        board_message_box('No weapon or armour damage inflicted.')
                        pygame.display.update()
                        pygame.time.wait(PAUSE_TIME)

                    else:

                        # Item is damaged so remove it
                        damage_item_name = items.get(damage_item).get('name')
                        board_message_box(damage_item_name + ' is destroyed.')

                        if turn == 'Opponent':
                            position = player_items.index(damage_item)
                            player_items[position] = 'Empty'
                        else:
                            position = opponent_items.index(damage_item)
                            opponent_items[position] = 'Empty'

                        pygame.display.update()
                        pygame.time.wait(PAUSE_TIME)

            else:

                # Attack has failed
                board_message_box('Attack failed!')

                pygame.display.update()
                pygame.time.wait(PAUSE_TIME)


            # Is player or opponent health 0 or less?
            if player_health <= 0:
                board_message_box('You have been defeated by ' + opponent.get('name') + '!')
            elif opponent_health <=0:

                # Boost player health with random value
                health_boost = random.randint(1, 3) * level

                board_message_box('You have defeated ' + opponent.get('name') + '. Your health is boosted by ' + str(health_boost) + '.')
                player_character['health'] = player_health + health_boost

                pygame.display.update()
                pygame.time.wait(PAUSE_TIME)

                # Give player any gold the opponent had
                gold = opponent.get('gold')
                player_character['gold'] = player_character.get('gold') + gold

                reward_item = people.win_new_item(level, items)
                reward_item_name = items.get(reward_item).get('name')
                reward_item_type = items.get(reward_item).get('type')
                board_message_box('You have won ' + str(gold) + ' gold pieces and also receive a ' + reward_item_name + '.')

                # If reward is a shield, replace existing shield
                if reward_item_type == 'Shield':
                    player_items[len(player_items) - 1] = reward_item
                else:

                    # If reward is not a shield, find first Empty slot
                    for item_counter, inventory_item in enumerate(player_items):
                        if inventory_item == 'Empty':
                            player_items[item_counter] = reward_item
                            break

                pygame.display.update()
                pygame.time.wait(PAUSE_TIME)

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
                         'You have earned ' + str(final_gold) + ' gold pieces as your reward'])
    else:
        overlay_message(['Like many who came before, you have fallen in the ancient city of Shadowstone.',
                         '',
                         'There will be many others who foolishly follow in your steps.'])

    pygame.display.update()

    return_pressed = False

    while return_pressed is False:

        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()

            if key_pressed[pygame.K_RETURN]:
                return_pressed = True

        check_for_quit(event)





def check_for_quit(event):
    if event.type == QUIT:
        pygame.quit()
        sys.exit()


# Display the player characters to be chosen from
def display_choose_characters(characters):

    # set up cards and names
    player_a_card_image = characters.get('Player A').get('image')
    player_b_card_image = characters.get('Player B').get('image')
    player_c_card_image = characters.get('Player C').get('image')
    player_d_card_image = characters.get('Player D').get('image')

    player_a_name = characters.get('Player A').get('name')
    player_b_name = characters.get('Player B').get('name')
    player_c_name = characters.get('Player C').get('name')
    player_d_name = characters.get('Player D').get('name')

    char_card_width = get_image_width(player_a_card_image)
    char_card_height = get_image_height(player_a_card_image)

    # display cards
    spacing = (SCREENWIDTH - char_card_width * 4) / 5
    row_y = spacing
    col_1_x = spacing
    col_2_x = char_card_width + 2 * spacing
    col_3_x = 2 * char_card_width + 3 * spacing
    col_4_x = 3 * char_card_width + 4 * spacing

    game_screen.blit(player_a_card_image, [col_1_x, row_y])
    game_screen.blit(player_b_card_image, [col_2_x, row_y])
    game_screen.blit(player_c_card_image, [col_3_x, row_y])
    game_screen.blit(player_d_card_image, [col_4_x, row_y])

    # display the numbers to choose a character below each card
    y_coordinate = row_y + char_card_height
    below_card_rect_height = 22

    #draw the boxed backgrounds to go below each card
    below_card_1_rect = (col_1_x, y_coordinate, char_card_width, below_card_rect_height)
    pygame.draw.rect(game_screen, BLACK, below_card_1_rect)

    below_card_2_rect = (col_2_x, y_coordinate, char_card_width, below_card_rect_height)
    pygame.draw.rect(game_screen, BLACK, below_card_2_rect)

    below_card_3_rect = (col_3_x, y_coordinate, char_card_width, below_card_rect_height)
    pygame.draw.rect(game_screen, BLACK, below_card_3_rect)

    below_card_4_rect = (col_4_x, y_coordinate, char_card_width, below_card_rect_height)
    pygame.draw.rect(game_screen, BLACK, below_card_4_rect)

    # display the numbers
    centre_text_with_object('Press 1', col_1_x, char_card_width, y_coordinate, WHITE)
    centre_text_with_object('Press 2', col_2_x, char_card_width, y_coordinate, WHITE)
    centre_text_with_object('Press 3', col_3_x, char_card_width, y_coordinate, WHITE)
    centre_text_with_object('Press 4', col_4_x, char_card_width, y_coordinate, WHITE)

    # display names
    y_coordinate = row_y + char_card_height + CARDPADDING + below_card_rect_height
    centre_text_with_object(player_a_name, col_1_x, char_card_width, y_coordinate, BLACK)
    centre_text_with_object(player_b_name, col_2_x, char_card_width, y_coordinate, BLACK)
    centre_text_with_object(player_c_name, col_3_x, char_card_width, y_coordinate, BLACK)
    centre_text_with_object(player_d_name, col_4_x, char_card_width, y_coordinate, BLACK)

# Centre any piece of text with a given object
def centre_text_with_object (display_text, object_x, object_width, text_y_coord, text_color):

    text = font.render(display_text, True, text_color)
    text_rect = text.get_rect()
    text_x_coord = object_x + (object_width - text_rect.width) / 2

    game_screen.blit(text, [text_x_coord, text_y_coord])

# Display a level description
def display_description(level, next_opponent_name):
    all_levels = [['You arrive at the Kings Tavern, an old inn at the edge of the city. After a light ',
                   'refreshment, you notice a shadow from behind and when turning around you are ',
                   'met by '],

                  ['You walk out into the town square. The low sun casts shadows all around as ',
                   'you edge your way towards the old cathedral at the far end of the square. Just ',
                   'as your eyes are adjusting you notice a figure moving out of a doorway. It is '],

                  ['The doors to the old cathedral swing open. Slowly you edge your way through the  ',
                   'town square to the entrance. It is cold and gloomy inside but through the darkness ',
                   'you can just about make out a in the far corner. The shape is waiting for you - '],
                  ]

    level_text = all_levels[level - 1]
    last_line = len(level_text) - 1
    level_text[last_line] += next_opponent_name + '.'
    overlay_message(level_text)

# Display a message on screen taking in a list of lines of text to be displayed
def overlay_message(text_to_display):

    number_of_lines = len(text_to_display)

    box_left = PRINTBOXMARGIN
    box_top = (SCREENHEIGHT - (number_of_lines + 4 )* PRINTLINESIZE) / 2

    box_width = SCREENWIDTH - 2 * PRINTBOXMARGIN
    box_height = (number_of_lines + 4) * PRINTLINESIZE

    message_rect = (box_left, box_top, box_width, box_height)
    pygame.draw.rect(game_screen, DARKBLUE, message_rect)

    for line_number, line in enumerate(text_to_display):
        display_line = font.render(line, True, WHITE)

        message_loc = [PRINTBOXMARGIN + PRINTLINESIZE, box_top + PRINTLINESIZE + line_number * PRINTLINESIZE]
        game_screen.blit(display_line, message_loc)

    # Add a final line of text to tell the user to hit RETURN
    final_line = font.render('[Hit RETURN to continue]', True, WHITE)
    final_line_rect = final_line.get_rect()
    final_line_loc = [(SCREENWIDTH - final_line_rect.width) / 2, box_top + 2 * PRINTLINESIZE + number_of_lines * PRINTLINESIZE]
    game_screen.blit(final_line, final_line_loc)

# Display a centred message across the middle band of the board
def board_message_box(message):
    """message_box_left = CARDPADDING
    message_box_top = SCREENHEIGHT / 2 - 2 * PRINTLINESIZE
    message_box_width = SCREENWIDTH - 2 * CARDPADDING
    message_box_height = 4 * PRINTLINESIZE
    message_box_right = SCREENWIDTH - CARDPADDING
    message_box_bottom = SCREENHEIGHT / 2 + 2 * PRINTLINESIZE

    #message_rect = (message_box_left, message_box_top, message_box_width, message_box_height)
    #pygame.draw.rect(game_screen, BIEGE, message_rect)

    draw_box(message_box_left, message_box_top, message_box_right, message_box_bottom, GREY, 3)"""
    message_box_width = SCREENWIDTH - 2 * LEFTMARGIN
    game_screen.blit(message_box_image, [LEFTMARGIN, SCREENHEIGHT / 2 - 2 * PRINTLINESIZE ])
    centre_text_with_object(message, LEFTMARGIN, message_box_width, (SCREENHEIGHT - PRINTLINESIZE) /2, BLACK)

# Display the main board
def display_board(opponent, player, opponent_items, player_items, items):
    player_card_image = player.get('image')
    card_width = get_image_width(player_card_image)
    card_height = get_image_height(player_card_image)
    empty_item_image = items.get('Empty').get('image')
    item_width = get_image_width(empty_item_image)
    item_height = get_image_height(empty_item_image)
    #card_x = (SCREENWIDTH - card_width) / 2

    # display opponent
    opponent_card_image = opponent.get('image')
    opponent_card_y = SCREENHEIGHT - card_height - CARDPADDING
    game_screen.blit(opponent_card_image, [CARD_X, opponent_card_y])

    # display player

    player_card_y = CARDPADDING
    game_screen.blit(player_card_image, [CARD_X, player_card_y])

    # Draw display boxes
    box_left = LEFTMARGIN
    #box_right = CARDPADDING + CARD_X - 2 * CARDPADDING
    opponent_box_top = opponent_card_y
    opponent_box_bottom = opponent_card_y + card_height
    player_box_top = player_card_y
    player_box_bottom = player_card_y + card_height
    #box_width = CARD_X - 2 * LEFTMARGIN

    box_height = card_height

    #opponent_rect = (box_left, opponent_box_top, box_width, box_height)
    #pygame.draw.rect(game_screen, BIEGE, opponent_rect)

    game_screen.blit(stats_box_image, [box_left, opponent_card_y])
    game_screen.blit(stats_box_image, [box_left, player_card_y])
    #draw_box(box_left, opponent_box_top, box_right, opponent_box_bottom, GREY, 3)

    #player_rect = (box_left, player_box_top, box_width, box_height)
    #pygame.draw.rect(game_screen, BIEGE, player_rect)

    #draw_box(box_left, player_box_top, box_right, player_box_bottom, GREY, 3)


    y_coordinate = opponent_box_top + CARDPADDING
    #centre_text_with_object(opponent_name, box_left, box_width, y_coordinate, BLACK)



    y_coordinate = player_box_top + CARDPADDING
    #centre_text_with_object(player_name, box_left, box_width, y_coordinate, BLACK)

    # Display stats
    opponent_name = opponent.get('name')
    display_stats(opponent_name, opponent_box_top, 0)


    opponent_hea_text = 'Health: ' + str(opponent.get('health'))
    display_stats(opponent_hea_text, opponent_box_top, 2)

    opponent_str_text = 'Strength: ' + str(opponent.get('strength'))
    display_stats(opponent_str_text, opponent_box_top, 3)

    opponent_dex_text = 'Dexterity: ' + str(opponent.get('dexterity'))
    display_stats(opponent_dex_text, opponent_box_top, 4)

    opponent_mag_text = 'Magic: ' + str(opponent.get('magic'))
    display_stats(opponent_mag_text, opponent_box_top, 5)

    opponent_gold_text = 'Gold: ' + str(opponent.get('gold'))
    display_stats(opponent_gold_text, opponent_box_top, 6)

    player_name = player.get('name')
    display_stats(player_name, player_box_top, 0)

    player_hea_text = 'Health: ' + str(player.get('health'))
    display_stats(player_hea_text, player_box_top, 2)

    player_str_text = 'Strength: ' + str(player.get('strength'))
    display_stats(player_str_text, player_box_top, 3)

    player_dex_text = 'Dexterity: ' + str(player.get('dexterity'))
    display_stats(player_dex_text, player_box_top, 4)

    player_mag_text = 'Magic: ' + str(player.get('magic'))
    display_stats(player_mag_text, player_box_top, 5)

    player_gold_text = 'Gold: ' + str(player.get('gold'))
    display_stats(player_gold_text, player_box_top, 6)

    # Display player items
    for item_no, player_item in enumerate(player_items):
        item = items.get(player_item)
        item_image = item.get('image')
        item_type = item.get('type')

        item_value = 0
        if item_type == 'Weapon':
            item_value = item.get('attack')
        elif item_type == 'Shield' or item_type == 'Armour':
            item_value = item.get('defence')

        # If item_no is 0 - 2 then display on first line
        if item_no < 3:
            item_x = ITEM_X[item_no] #+ card_width + 2 * CARDPADDING + item_no * (item_width + CARDPADDING)
            item_y = player_card_y

        # If item no is 3 - 5 then display on second line
        else:
            item_x = ITEM_X[item_no - 3] #+ card_width + 2 * CARDPADDING + (item_no - 3) * (item_width + CARDPADDING)
            item_y = player_card_y + item_height + PRINTLINESIZE

        game_screen.blit(item_image, [item_x, item_y])

        # Display the attack / defence value of the item if it has one
        if item_value > 0:
            display_item_value(item_x + item_width, item_y + item_height, item_value)

        below_item_rect = (item_x, item_y + item_height, item_width, PRINTLINESIZE)
        #pygame.draw.rect(game_screen, BIEGE, below_item_rect)

        # If item_no is between 0 & 4 it's a weapon so display the item number (+1 to make it 1-5)
        if item_no < 5:
            centre_text_with_object(str(item_no + 1), item_x, item_width, item_y + item_height, BLACK)


    # Display opponent items
    for opponent_item_no, opponent_item in enumerate(opponent_items):
        opp_item = items.get(opponent_item)
        opp_item_image = opp_item.get('image')
        opp_item_type = opp_item.get('type')

        opp_item_value = 0
        if opp_item_type == 'Weapon':
            opp_item_value = opp_item.get('attack')
        elif opp_item_type == 'Shield' or opp_item_type == 'Armour':
            opp_item_value = opp_item.get('defence')

        # If item_no is 0 - 2 then display on first line
        if opponent_item_no < 3:
            item_x = ITEM_X[opponent_item_no] #CARD_X + card_width + 2 * CARDPADDING + opponent_item_no * (item_width + CARDPADDING)
            item_y = opponent_card_y

        # If item no is 3 - 5 then display on second line
        else:
            item_x = ITEM_X[opponent_item_no - 3] # CARD_X + card_width + 2 * CARDPADDING + (opponent_item_no - 3) * (item_width + CARDPADDING)
            item_y = opponent_card_y + item_height + PRINTLINESIZE

        game_screen.blit(opp_item_image, [item_x, item_y])

        # Display the attack / defence value of the item if it has one
        if opp_item_value > 0:
            display_item_value(item_x + item_width, item_y + item_height, opp_item_value)

        below_item_rect = (item_x, item_y + item_height, item_width, PRINTLINESIZE)
        #pygame.draw.rect(game_screen, BIEGE, below_item_rect)




# Select a random weapon for the opponent to attack with
def get_opponent_weapon(opponent_items, items):

    # Select a random item from the opponent's list of items
    random_item_name = random.choice(opponent_items)
    random_item = items.get(random_item_name)
    random_item_type = random_item.get('type')

    # Make sure it is a weapon, if not keep selecting another random item until a weapon is chosen
    while random_item_type != 'Weapon':
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

    attack_score = attacker_strength * STRENGTH_ATTACK_MULTIPLIER \
                   + attacker_dexterity * DEXTERITY_ATTACK_MULTIPLIER \
                   + attacker_weapon_attack * WEAPON_ATTACK_MULTIPLIER

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

    defence_score = defender_strength * STRENGTH_DEFENCE_MULTIPLIER + \
                    defender_dexterity * DEXTERITY_DEFENCE_MULTIPLIER + \
                    armour_defence * ARMOUR_DEFENCE_MULTIPLIER

    defence_score = int(defence_score / 6)

    # If attack and defence are the same, looking to roll a 10 or more
    # If attack is much stronger than defence, then a lower (than 10) score required
    # If defence is much stronger than attack, then a higher (than 10) score required
    dice_score = 10 - int((attack_score - defence_score) / 2)
    if dice_score > 20:
        dice_score = 20
    elif dice_score < 1:
        dice_score = 1

    return(dice_score)

# Format the display of the board game stats, aligned with the relevant card (horizontally)
def display_stats(display_text, box_top, line_no):
    text_x_coord = LEFTMARGIN = 20 + CARDPADDING
    text_y_coord = box_top + 2 * CARDPADDING + PRINTLINESIZE * line_no

    text = font.render(display_text, True, BLACK)
    game_screen.blit(text, [text_x_coord, text_y_coord])

# Display a banner reading 'TURN' over a character card to indicate whose turn is being played
def draw_turn_banner(turn, card_width, card_height):
    rect_x = CARD_X #(SCREENWIDTH - card_width) / 2

    """text = small_font.render('TURN', True, WHITE)
    text_rect = text.get_rect()
    text_width = text_rect.width
    text_height = text_rect.height"""

    if turn == 'Player':
        rect_y = CARDPADDING + card_height - PRINTLINESIZE
    else:
        rect_y = SCREENHEIGHT - CARDPADDING - PRINTLINESIZE

    game_screen.blit(turn_image, [rect_x, rect_y])

    """turn_rect = (rect_x, rect_y , card_width, PRINTLINESIZE)
    pygame.draw.rect(game_screen, GREEN, turn_rect)

    text_x = (SCREENWIDTH - text_width) / 2
    text_y = rect_y + (PRINTLINESIZE - text_height) / 2

    game_screen.blit(text, [text_x, text_y])"""

# Display the item attack / defence value in the bottom right of each item box
def display_item_value (item_box_right, item_box_bottom, item_score):
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

# Display the dice with a given value / colour
def display_dice(dice_value, dice_colour):
    dice_size = 60


    #dice_rect = ((SCREENWIDTH - dice_size) / 2, (SCREENHEIGHT - dice_size) / 2, dice_size, dice_size)
    #dice_x = (SCREENWIDTH - dice_1_image.get_rect().width) / 2
    #dice_y = (SCREENHEIGHT - dice_1_image.get_rect().height) / 2
    game_screen.blit(dice_15_image, [DICE_X, DICE_Y])

    """text = large_font.render(str(dice_value), True, WHITE)
    text_rect = text.get_rect()
    text_width = text_rect.width
    text_height = text_rect.height

    text_x_coord = (SCREENWIDTH - text_width) / 2
    text_y_coord = (SCREENHEIGHT - text_height) / 2

    game_screen.blit(text, [text_x_coord, text_y_coord])"""

# Calculate the width of an image
def get_image_width(image):
    image_width = image.get_rect().width
    return image_width

# Calculate the height of an image
def get_image_height(image):
    image_height = image.get_rect().height
    return image_height


if __name__ == "__main__":
    main()
