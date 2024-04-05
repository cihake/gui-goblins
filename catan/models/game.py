from django.db import models
"""
Game overhead. It stores the players, along with flags for turn progression
and multi-step interaction.
"""
class Game(models.Model):
    number_players = models.IntegerField()
    turn = models.IntegerField()