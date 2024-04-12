from django.db import models
"""
A player of the game. They have an ordinal (which player they are),
the space that their piece is on, and a money total.
"""
class Player(models.Model):
    ordinal = models.IntegerField()
    space = models.IntegerField()
    money = models.IntegerField()