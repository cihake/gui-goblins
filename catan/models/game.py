from django.db import models
"""
Game overhead. It stores the players, along with flags for turn progression
and multi-step interaction.
"""
class Game(models.Model):
    game_key = models.UUIDField(unique=True)
    turn = models.IntegerField(default=1)
    number_players = models.IntegerField(default=1)
    # Flag for setup; also indicates the "turn" of setup
    setup_flag = models.IntegerField(default=1)
    # Flag for building; 0 = no build, 1 = settlement
    build_flag = models.IntegerField(default=0)
