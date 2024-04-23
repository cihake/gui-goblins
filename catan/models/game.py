from django.db import models
"""
Game overhead. It stores the players, along with flags for turn progression
and multi-step interaction.
The setup flag can refer to the player setting up, and the build flag can refer
to multiple kinds of building; 0 = no build, 1 = settlement, 2 = road start, 3 = road end
"""
class Game(models.Model):
    game_key = models.UUIDField(unique=True)
    turn = models.IntegerField(default=1)
    number_players = models.IntegerField(default=1)
    setup_flag = models.IntegerField(default=1)
    build_flag = models.IntegerField(default=0)
