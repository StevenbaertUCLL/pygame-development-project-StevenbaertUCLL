#adding modules
import copy
import random
import pygame
#import tkinter.font as font

#game variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 8
game_deck = copy.deepcopy(decks * one_deck)
my_hand = []
my_hand_2 = []
dealer_hand = []
outcome = 0
records = [0, 0, 0]  #win, los and draws
player_score = 0
dealer_score = 0
player_score_2 = 0
split_button = []
start_new = []

#defining the display screen
pygame.init()
WIDTH = 900
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.SysFont('arial', 49)
active = False
initial_deal = False
reveal_dealer = False
hand_active = False
add_score = False
run = True
possible_split = False
split_stack = False
new_deck = False
busted_hand_1 = False
busted_hand_2 = False

text = ['', 'Player busted', 'Player Wins', 'Dealer wins', 'Tie game']

#function to start the dealing of inital cards
def deal_cards(hand, current_deck):
    card = random.randint(0, len(current_deck))
    hand.append(current_deck[card - 1])
    current_deck.pop(card - 1)
    return hand, current_deck

# draw cards on screen
def draw_card(player, dealer, reveal, player_split, hand_1, hand_2):
    #when there is one stack
    if split_stack == False:
        for i in range(len(player)):
            pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
            screen.blit(font.render(player[i], True, 'black'), (140 + (70 * i), 465 + (5 * i)))
            screen.blit(font.render(player[i], True, 'black'), (75 + (70 * i), 615 + (5 * i)))
            pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)
    #with 2 stacks
    else:
        for i in range(len(player)):
            pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
            screen.blit(font.render(player[i], True, 'black'), (140 + (70 * i), 465 + (5 * i)))
            screen.blit(font.render(player[i], True, 'black'), (75 + (70 * i), 615 + (5 * i)))
            pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)
        for j in range(len(player_split)):
            pygame.draw.rect(screen, 'white', [470 + (70 * j), 460 + (5 * j), 120, 220], 0, 5)
            screen.blit(font.render(player_split[j], True, 'black'), (540 + (70 * j), 465 + (5 * j)))
            screen.blit(font.render(player_split[j], True, 'black'), (475 + (70 * j), 615 + (5 * j)))
            pygame.draw.rect(screen, 'red', [470 + (70 * j), 460 + (5 * j), 120, 220], 5, 5)
    #draws a message when a hands busts
    if hand_1:
            pygame.draw.rect(screen, 'white', [120, 530, 225, 100], 0, 5) #drawing of a rectangle to start the deal
            pygame.draw.rect(screen, 'black', [120, 530, 225, 100], 3, 5)
            bust_1_text = font.render( 'Busted', True, 'black')
            screen.blit(bust_1_text, (165, 550))
    if hand_2:
            pygame.draw.rect(screen, 'white', [540, 530, 225, 100], 0, 5) #drawing of a rectangle to start the deal
            pygame.draw.rect(screen, 'black', [540, 530, 225, 100], 3, 5)
            bust_2_text = font.render( 'Busted', True, 'black')
            screen.blit(bust_2_text, (585, 550))

#drawing the dealers cards
    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (140 + (70 * i), 165 + (5 * i)))
            screen.blit(font.render(dealer[i], True, 'black'), (75 + (70 * i), 315 + (5 * i)))
        else:
            screen.blit(font.render('???', True, 'black'), (140 + (70 * i), 165 + (5 * i)))
            screen.blit(font.render('???', True, 'black'), (75 + (70 * i), 315 + (5 * i)))
        pygame.draw.rect(screen, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)

#function to draw everything from the game
def draw_game(act, record, result, split_box, new_game):
    button_list = []
    start_new = []
    split_button = []
    # buttons visible on start up(Not active)
    if not act and not new_game:
        deal = pygame.draw.rect(screen, 'white', [150, 20, 225, 100], 0, 5) #drawing of a rectangle to start the deal
        pygame.draw.rect(screen, 'green', [150, 20, 225, 100], 3, 5)
        deal_text = font.render( 'Deal Hand', True, 'black')
        screen.blit(deal_text, (165, 50)) #defining the text in the rectangle
        button_list.append(deal)

    else:
        #drawing of the split boxes when the possibility of a split comes up
        if split_box:
            pygame.draw.rect(screen, 'white',[550, 580, 225, 100], 0, 5) #rectangle with split? in it
            split_text = font.render('Split?', True, 'black')
            screen.blit(split_text, (610,600))

            #drawing of the yes and no button
            yes = pygame.draw.rect(screen, 'white',[550, 700, 110, 100], 0, 5) #rectangle with Yes in it with a green frame
            pygame.draw.rect(screen, 'green', [550, 700, 110, 100], 3, 5)
            yes_text = font.render('Yes', True, 'black')
            screen.blit(yes_text, (575, 735))
            split_button.append(yes)

            no = pygame.draw.rect(screen, 'white',[670, 700, 110, 100], 0, 5) #rectangle with No in it with a green frame
            pygame.draw.rect(screen, 'green', [670, 700, 110, 100], 3, 5)
            no_text = font.render('No', True, 'black')
            screen.blit(no_text, (695, 735))
            split_button.append(no)
        #drawing of a box when the deck is below 9 cards
        if new_game:
            pygame.draw.rect(screen, 'white', [350, 580, 225, 100], 0, 5) #rectangle with New Deck in it.
            new_text = font.render('New Deck?', True, 'black')
            screen.blit(new_text, (350,600))

            yes = pygame.draw.rect(screen, 'white',[350, 700, 110, 100], 0, 5) #rectangle with Yes in it with a green frame
            pygame.draw.rect(screen, 'green', [350, 700, 110, 100], 3, 5)
            yes_text = font.render('Yes', True, 'black')
            screen.blit(yes_text, (375, 735))
            start_new.append(yes)

            no = pygame.draw.rect(screen, 'white',[470, 700, 110, 100], 0, 5) #rectangle with No in it with a Red frame
            pygame.draw.rect(screen, 'red', [470, 700, 110, 100], 3, 5)
            no_text = font.render('No', True, 'black')
            screen.blit(no_text, (495, 735))
            start_new.append(no)      

        if not new_game:    #button to get a new card
            hit = pygame.draw.rect(screen, 'white', [50, 700, 225, 100], 0, 5) #drawing of a rectangle for the hit
            pygame.draw.rect(screen, 'green', [50, 700, 225, 100], 3, 5)
            hit_text = font.render( 'New card', True, 'black')
            screen.blit(hit_text, (75, 735))
            button_list.append(hit)

            # button to stop getting cards
            stand = pygame.draw.rect(screen, 'white', [300, 700, 225, 100], 0, 5) #drawing of a rectangle for the stand
            pygame.draw.rect(screen, 'green', [300, 700, 225, 100], 3, 5)
            stand_text = font.render( 'Stand', True, 'black')
            screen.blit(stand_text, (355, 735)) #defining the text in the rectangle
            button_list.append(stand)
            # collection of the wins/losses/draws
            score_text = font.render(f'Wins: {record[0]}    Losses: {record[1]}     Draws: {record[2]}', True, 'white')
            screen.blit(score_text, (15, 840))

    #check for the outcome, and display reset button and to see what happend
    if result != 0:
        screen.blit(font.render(text[result], True, 'white'), (15, 25))
        deal = pygame.draw.rect(screen, 'white', [150, 220, 225, 100], 0, 5) #drawing of a rectangle to start the deal
        pygame.draw.rect(screen, 'green', [150, 220, 225, 100], 3, 5)
        pygame.draw.rect(screen, 'black', [150, 223, 221, 94], 3, 5)
        deal_text = font.render( 'New Hand', True, 'black')
        screen.blit(deal_text, (165, 250)) #defining the text in the rectangle
        button_list.append(deal)

    return button_list, split_button, start_new      

#calculate the score and see the aces
def calculate_score(hand):
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        #calc the numeric values except 10
            for j in range(8):
                if hand[i] == cards[j]:
                    hand_score += int(hand[i])
        #for 10 and letters
            if hand[i] in ['10', 'J', 'Q', 'K']:
                hand_score += 10
        #check aces as 11, check later if aces should be 1 or 11
            elif hand[i] == 'A':
                hand_score += 11     
    #check the aces to see if it needs to be 11 or 1
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score

#draw the scores on the screen
def draw_scores(player, dealer, player_split):
    #drawing of the scores below the buttons
    if split_stack == False: 
        screen.blit(font.render(f'Score {player}', True, 'White'), (350, 400))
    else:
        screen.blit(font.render(f'Score stack: {player}', True, 'White'), (50, 400))
        screen.blit(font.render(f'Score stack 2: {player_split}', True, 'White'), (450, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Score {dealer}', True, 'White'), (350, 100))

def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    #check different end scenario's
    # result 1-Bust; 2 - win, 3-loss, 4-tie
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
    return result, totals, add

def split(hand):
    #Function to make 2 hands from 1 hand
    hand_1 = []
    hand_2 = []
    hand_1.append(hand[0])
    hand_2.append(hand[1])
    splitted = True
    return hand_1, hand_2, splitted
    
#Main loop

while run:
    # run game at frame rate define screen with colour
    timer.tick(fps)
    screen.fill('black')
    # initial deal player/dealer
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            initial_deal = False
        #check the length of the deck and stops the loop when the deck is less than 9
        if len(game_deck) <= 8:
            new_deck = True
            active = False
            initial_deal = False
            my_hand = []
        #check if the 2 initial cards can be split
        if not new_deck:
            if my_hand[0] == my_hand[1]:
                possible_split = True
    #to calculate the player score and the dealer score     
    if active and not split_stack:
        player_score = calculate_score(my_hand)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_card(my_hand, dealer_hand, reveal_dealer, my_hand_2, busted_hand_1, busted_hand_2)
        draw_scores(player_score, dealer_score, player_score_2)
    #to calculate the player score that use 2 stacks and the dealer score
    if active and split_stack:
        player_score = calculate_score(my_hand)
        player_score_2 = calculate_score(my_hand_2)
        if player_score > 21:
            busted_hand_1 = True
        elif player_score_2 > 21:
            busted_hand_2 = True
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_card(my_hand, dealer_hand, reveal_dealer, my_hand_2, busted_hand_1, busted_hand_2)
        draw_scores(player_score, dealer_score, player_score_2)

    #draws the game with 3 lists of buttons    
    buttons, split_button, start_new = draw_game(active, records, outcome, possible_split, new_deck)
  
    #button interactions for when pressing quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            #initial start of the game and the parameters
            if not active and not new_deck:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    outcome = 0
                    add_score = True
            #when clicking on yes or no when the option pops up to start a new deck
            elif new_deck:
                if start_new[0].collidepoint(event.pos):
                    game_deck = copy.deepcopy(decks * one_deck)
                    initial_deal = True
                    active = True
                    initial_deal = True
                    my_hand = []
                    dealer_hand = []
                    my_hand_2 = []
                    outcome = 0
                    hand_active = True
                    add_score = True
                    dealer_score = 0 
                    player_score = 0
                    player_score_2 = 0
                    reveal_dealer = False
                    split_stack = False
                    new_deck = False
                if start_new[1].collidepoint(event.pos):
                        run = False
            else:
                #main buttons when playing the game
                if possible_split:
                #buttons and the parameters for splitting
                    if split_button[0].collidepoint(event.pos):
                        my_hand, my_hand_2, split_stack = split(my_hand)
                        possible_split = False
                        split_stack = True
                    elif split_button[1].collidepoint(event.pos):
                        split_stack = False
                        possible_split = False
                if not split_stack and not new_deck:
                #buttons and the parameters in the main game loop
                    if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active and possible_split == False:
                        my_hand, game_deck = deal_cards(my_hand, game_deck)
                    elif buttons[1].collidepoint(event.pos) and not reveal_dealer and possible_split == False:
                        reveal_dealer = True
                        hand_active = False
                    elif len(buttons) == 3:
                        if buttons[2].collidepoint(event.pos):
                            active = True
                            initial_deal = True
                            my_hand = []
                            dealer_hand = []
                            my_hand_2 = []
                            outcome = 0
                            hand_active = True
                            add_score = True
                            dealer_score = 0 
                            player_score = 0
                            player_score_2 = 0
                            reveal_dealer = False
                elif split_stack:
                # buttons and actions when 2 stacks are active
                    if buttons[0].collidepoint(event.pos) and (player_score < 21 or player_score_2 < 21) and hand_active:
                    #drawing new cards with split and the possibility to only get cards for the active stacks
                        if busted_hand_1:
                            my_hand_2, game_deck = deal_cards(my_hand_2, game_deck)
                        elif busted_hand_2:
                            my_hand, game_deck = deal_cards(my_hand, game_deck)
                        else:
                            my_hand, game_deck = deal_cards(my_hand, game_deck)
                            my_hand_2, game_deck = deal_cards(my_hand_2, game_deck)
                    elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    #buttons and action when standing
                        reveal_dealer = True
                        hand_active = False
                    elif len(buttons) == 3:
                    #buttons and actions when restarting the game
                        if buttons[2].collidepoint(event.pos):
                            active = True
                            initial_deal = True
                            my_hand = []
                            dealer_hand = []
                            my_hand_2 = []
                            outcome = 0
                            hand_active = True
                            add_score = True
                            dealer_score = 0 
                            player_score = 0
                            player_score_2 = 0
                            reveal_dealer = False
                            split_stack = False
                            busted_hand_1 = False
                            busted_hand_2 = False
    #code to see which stack was closer to 21 or if both stacks passed 21 without pressing the stand button
    else:   
        if hand_active and ((player_score == 21 or player_score_2 == 21) or (player_score_2 > 21 and player_score > 21) ) and split_stack:
            hand_active = False
            reveal_dealer = True
            
        if hand_active and player_score >= 21 and not split_stack:
            hand_active = False
            reveal_dealer = True       
    if reveal_dealer:
        print(f'{player_score} and {player_score_2}')
        if (player_score > 21 and player_score_2 <= 21) or (player_score < player_score_2 <= 21):
            player_score = player_score_2    
            
    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)
    pygame.display.flip()       #everything froom display gets flipped on the screen
pygame.quit()  