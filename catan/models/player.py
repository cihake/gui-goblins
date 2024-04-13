from django.db import models
"""
A player of the game. They have an ordinal (which player they are)
and a resource total.
"""
class Player(models.Model):
    game_key = models.UUIDField(unique=True, null=True)
    ordinal = models.IntegerField(default=-1)
    wool = models.IntegerField(default=0)
    grain = models.IntegerField(default=0)
    lumber = models.IntegerField(default=0)
    brick = models.IntegerField(default=0)
    ore = models.IntegerField(default=0)

    