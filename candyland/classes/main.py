"""
The main function to run the game.
Most of the logic is handled via methods.
The game is played with three players.
"""

# import objects
#from board import Board
#from space import Space
#from deck import Deck
#from card import Card
from player import Player

class Main:
    #initialize variables and objects
    #board = Board()
    #deck = Deck()
    turn = 1
    player1 = Player(50, 50, 1, "null", "null")
    player2 = Player(50, 50, 2, "null", "null")
    player3 = Player(50, 50, 3, "null", "null")
    current_player = player1
    winner = 0

    # loop for turns
    """if (current_player.skip == False):
        # draw the new board, declaring the current player's turn
        # Interaction: wait for the player to draw a card, and show what they drew
        card = deck.draw_card()

        # if the deck is empty, shuffle it
        if (deck.is_empty): deck.shuffle()

        # act on the card draw; show the card

        # move the player: requires logic
        position = current_player.space
        if (card.special == 0): # a single-color card
            # Go forward from the current player's position to the next
            # space with the corresponding color
            for i in range(position, len(board.spaces)):
                if (position < len(board.spaces) and board.spaces[i] == card.value):
                    position = i
                    break
                elif (position == len(board.spaces)):
                    position = len(board.spaces)
        elif (card.special == 1): # a double-color card
            found = 0
            for i in range(position, len(board.spaces)):
                if (position < len(board.spaces) and board.spaces[i] == card.value):
                    found += 1
                if (found == 2):
                    position = i
                    break
                if (position == len(board.spaces)):
                    position = len(board.spaces)
        elif (card.special == 2): # a unique card
            for i in board.spaces:
                if (board.spaces[i] == card.value):
                    position = i
        
        # act on the landed space; jump, skip, or win
        if (board.spaces[position].value == "entrance1":
            for i in board.spaces:
            if (board.spaces[i].value == "exit1"):
                position = i
        elif (board.spaces[position].value == "entrance2":
            for i in board.spaces:
            if (board.spaces[i].value == "exit2"):
                position = i
        elif (board.spaces[position].skip == True):
            current_player.skip = True
        elif (position == len(board.spaces)):
            winner = current_player.ordinal
        
        """
    
    # go to the next turn
    """turn += 1
    current_player"""

    # declare a winner