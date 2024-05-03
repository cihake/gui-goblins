from django.db import models
from .player import Player
"""
Game overhead. It stores the players, along with flags for turn progression
and multi-step interaction.
The setup flag is for the setup phase of the game, and the build flag can refer to multiple
kinds of building; 0 = no build, 1 = settlement, 2 = road start, 3 = road end, 4 = city
"""
class Game(models.Model):
    game_key = models.UUIDField(unique=True)
    players = models.ManyToManyField('Player', related_name='games')
    number_players = models.IntegerField(default=1)
    current_player = models.IntegerField(default=1)
    previous_player = models.IntegerField(default=1)
    turn = models.IntegerField(default=1)
    setup_flag = models.IntegerField(default=1)
    build_flag = models.IntegerField(default=0)
    robber_flag = models.IntegerField(default=0)

    """Initialization; takes the game key, number of players, and number of starting settlements"""
    @classmethod
    def initialize(cls, game_key, number_players, starting_settlements):
        game = cls.objects.create(game_key=game_key, number_players=number_players)

        players = []
        for i in range(1, game.number_players+1):
            player = Player(ordinal=i, starting_settlements=starting_settlements)
            players.append(player)
        Player.objects.bulk_create(players)
        print("Players created:", [player.ordinal for player in players])
        game.players.add(*players)

        return game