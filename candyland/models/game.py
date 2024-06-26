from django.db import models
"""
Game overhead. It stores the players, along with flags for turn progression
and multi-step interaction.
"""
class Game(models.Model):
    game_key = models.UUIDField(unique=True)
    winner = models.IntegerField(default=0)
    turn = models.IntegerField(default=1)
    number_players = models.IntegerField(default=1)