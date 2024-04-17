from django.test import TestCase
import random
from monopoly.models.game import Game
from monopoly.models.player import Player
from monopoly.models.board import Board
from monopoly.models.space import Space
from monopoly.models.property_deck import PropertyDeck
from monopoly.models.property import Property
from monopoly.views import respond_to_space, tax_player, respond_to_property

class CatanTests(TestCase):
    def test(self):
        game = Game.objects.create(game_key="no key")
        player1 = Player.objects.create(game_key="no key", ordinal=1)
        board = Board.initialize("no key")
        property_deck = PropertyDeck.initialize("no key")

        """space response tests"""
        response = {}
        player1.space = 4 # Income Tax
        player1.money = 0
        respond_to_space(game, board, property_deck, player1, response)
        assert(player1.money == -200)
        player1.space = 14 # Virginia Avenue, buy
        player1.money = 0
        respond_to_space(game, board, property_deck, player1, response)
        assert(player1.money == -160)
        landed_property = property_deck.properties.get(index=7) # Virginia Avenue, collect
        landed_property.player = 1
        player1.money = 0
        respond_to_space(game, board, property_deck, player1, response)
        assert(player1.money == 12)