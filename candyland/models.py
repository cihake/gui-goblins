from django.db import models

"""
The board that the game is played on.
Positions are floats instead of integers to allow for scaling calculations.
Because of this, you may need to convert the values to integers
for certain functions. Remember; y goes down.
"""
class Board (models.Model):
    ypos = models.FloatField()
    xpos = models.FloatField()
    scale = models.FloatField()

"""
Spaces on the board for people to land on.
Their positions are also floats to allow for scaling calculations;
convert them to integers as needed. Their index is given by their
position on an ArrayList. Note that "pink" is a color, not a special.
"""
class Space(models.Model):
    ypos = models.FloatField()
    xpos = models.FloatField()
    color = models.CharField()
    special = models.CharField()

"""
A player character. Their position can be used for animations.
Their "ordinal" refers to which player they are (player 1,2).
Their "space" should correspond with the index of a Space object,
and is used to determine what Space to draw / move to.
The skip boolean determines whether or not their turn should be
skipped this round.
"""
class Player(models.Model):
    ypos = models.FloatField()
    xpos = models.FloatField()
    ordinal = models.IntegerField()
    space = models.IntegerField()
    skip = models.BooleanField()

"""The deck is necessary to hold, shuffle, and distribute cards."""
class Deck(models.Model):
    ypos = models.FloatField()
    xpos = models.FloatField()

"""
A card from the deck. Its value corresponds with either the color
or special of a space.
"""
class Card(models.Model):
    value = models.CharField()