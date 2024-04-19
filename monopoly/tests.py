from django.test import TestCase
import random, uuid
from monopoly.models.game import Game
from monopoly.models.player import Player
from monopoly.models.board import Board
from monopoly.models.space import Space
from monopoly.models.property_deck import PropertyDeck
from monopoly.models.property import Property
from .view_methods import respond_to_space, tax_player, respond_to_property

class CatanTests(TestCase):
    def test(self):
        dummy_key = uuid.uuid4()
        game = Game.objects.create(game_key=dummy_key)
        player1 = Player.objects.create(game_key=dummy_key, ordinal=1)
        board = Board.initialize(dummy_key)
        property_deck = PropertyDeck.initialize(dummy_key)

        """space response tests"""
        response = {}
        player1.space = 4 # Income Tax
        player1.money = 0
        player1.save()
        respond_to_space(game, board, property_deck, player1, response)
        player1.save()
        assert(player1.money == -200)
        player1.space = 14 # Virginia Avenue, buy
        player1.money = 0
        player1.save()
        respond_to_space(game, board, property_deck, player1, response)
        player1.save()
        assert(player1.money == -160)
        landed_property = property_deck.properties.get(index=7) # Virginia Avenue, collect
        landed_property.player = 1
        landed_property.save()
        player1.money = 0
        player1.save()
        respond_to_space(game, board, property_deck, player1, response)
        player1.save()
        assert(player1.money == 12)