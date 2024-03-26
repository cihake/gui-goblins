"""
A deck of cards
It has an array of card objects.
The deck can shuffle the cards, draw a card from the itself,
and check if the deck is empty.
"""

from card import Card
import random

class Deck:
    cards = [] # an array to hold the cards
    deck_index = 0 # the position in the array
    def __init__(self, ypos=100, xpos=100, scale=1):
        self.ypos = ypos
        self.xpos = xpos
        self.scale = scale

        """add the cards to the deck.
        There are 6 singles for each color, 4 doubles for red, purple,
        yellow, blue, 3 doubles for orange and green, and the character
        cards. Overall, there are 62 cards in total."""
        for i in range(0, 5): self.cards.append(Card("red", 0, "null"))
        for i in range(0, 3): self.cards.append(Card("red", 1, "null"))
        for i in range(0, 5): self.cards.append(Card("purple", 0, "null"))
        for i in range(0, 3): self.cards.append(Card("purple", 1, "null"))
        for i in range(0, 5): self.cards.append(Card("yellow", 0, "null"))
        for i in range(0, 3): self.cards.append(Card("yellow", 1, "null"))
        for i in range(0, 5): self.cards.append(Card("blue", 0, "null"))
        for i in range(0, 3): self.cards.append(Card("blue", 1, "null"))
        for i in range(0, 5): self.cards.append(Card("orange", 0, "null"))
        for i in range(0, 2): self.cards.append(Card("orange", 1, "null"))
        for i in range(0, 5): self.cards.append(Card("green", 0, "null"))
        for i in range(0, 2): self.cards.append(Card("green", 1, "null"))
        self.cards.append(Card("peppermint", 2, "null"))
        self.cards.append(Card("peanut", 2, "null"))
        self.cards.append(Card("lollipop", 2, "null"))
        self.cards.append(Card("frosted", 2, "null"))

        # shuffle the newly-created deck
        self.shuffle


    """Shuffle the deck:
    Go through each card in the deck and swap it with another card"""
    def shuffle(self):
        for i in self.cards:
            random_index = random.randint(0, len(self.cards) - 1)
            swap = self.cards[random_index]
            self.cards[random_index] = self.cards[i]
            self.cards[i] = swap


    """Draw a card from the deck. (just increments the index)"""
    def draw_card(self):
        self.deck_index += 1


    """Check if the deck is empty"""
    def is_empty(self):
        if (self.deck_index == len(self.cards)): return True
        else: return False