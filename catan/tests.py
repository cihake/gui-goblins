from django.test import TestCase
import random
from catan.models.game import Game
from catan.models.player import Player
from catan.models.board import Board
from catan.models.corner import Corner
from catan.models.tile import Tile
from catan.views import build_attempt, gather_resources

class CatanTests(TestCase):
    def test(self):
        game = Game.objects.create(game_key="no key")
        board = Board.initialize("no key")
        player1 = Player.objects.create(game_key="no key", ordinal=1)
        
        """neighbor method tests"""
        corner = Corner.objects.create(yindex=3, xindex=4, building=0)
        neighbor_corners = board.get_neighbor_corners(corner)
        for Corner in neighbor_corners:
            self.assertTrue(Corner.xindex == 3 and Corner.yindex == 2 or
                            Corner.xindex == 4 and Corner.yindex == 2 or
                            Corner.xindex == 4 and Corner.yindex == 4)
        neighbor_tiles = board.get_neighbor_tiles(corner)
        for Tile in neighbor_tiles:
            self.assertTrue(Tile.xindex == 3 and Tile.yindex == 0 or
                            Tile.xindex == 3 and Tile.yindex == 1 or
                            Tile.xindex == 4 and Tile.yindex == 1)
        
        corner = Corner.objects.create(yindex=4, xindex=3, building=0)
        neighbor_corners = board.get_neighbor_corners(corner)
        for Corner in neighbor_corners:
            self.assertTrue(Corner.xindex == 3 and Corner.yindex == 3 or
                            Corner.xindex == 2 and Corner.yindex == 5 or
                            Corner.xindex == 3 and Corner.yindex == 5)
        neighbor_tiles = board.get_neighbor_tiles(corner)
        for Tile in neighbor_tiles:
            self.assertTrue(Tile.xindex == 2 and Tile.yindex == 1 or
                            Tile.xindex == 3 and Tile.yindex == 1 or
                            Tile.xindex == 2 and Tile.yindex == 2)
            
        corner = Corner.objects.create(yindex=5, xindex=4, building=0)
        neighbor_corners = board.get_neighbor_corners(corner)
        for Corner in neighbor_corners:
            self.assertTrue(Corner.xindex == 4 and Corner.yindex == 4 or
                            Corner.xindex == 5 and Corner.yindex == 4 or
                            Corner.xindex == 4 and Corner.yindex == 6)
        neighbor_tiles = board.get_neighbor_tiles(corner)
        for Tile in neighbor_tiles:
            self.assertTrue(Tile.xindex == 4 and Tile.yindex == 1 or
                            Tile.xindex == 3 and Tile.yindex == 2 or
                            Tile.xindex == 4 and Tile.yindex == 2)
            
        corner = Corner.objects.create(yindex=6, xindex=3, building=0)
        neighbor_corners = board.get_neighbor_corners(corner)
        for Corner in neighbor_corners:
            self.assertTrue(Corner.xindex == 3 and Corner.yindex == 5 or
                            Corner.xindex == 3 and Corner.yindex == 7 or
                            Corner.xindex == 4 and Corner.yindex == 7)
        neighbor_tiles = board.get_neighbor_tiles(corner)
        for Tile in neighbor_tiles:
            self.assertTrue(Tile.xindex == 2 and Tile.yindex == 2 or
                            Tile.xindex == 3 and Tile.yindex == 2 or
                            Tile.xindex == 3 and Tile.yindex == 3)
            
        corner = Corner.objects.create(yindex=8, xindex=0, building=0)
        neighbor_corners = board.get_neighbor_corners(corner)
        for Corner in neighbor_corners:
            self.assertTrue(Corner.xindex == 0 and Corner.yindex == 7 or
                            Corner.xindex == 0 and Corner.yindex == 9)
        neighbor_tiles = board.get_neighbor_tiles(corner)
        for Tile in neighbor_tiles:
            self.assertTrue(Tile.xindex == 0 and Tile.yindex == 3)
        
        """build attempt method tests"""
        response = {}
        # not touching land
        corner = board.corners.get(yindex=0, xindex=0)
        build_attempt(board, corner.yindex, corner.xindex, response)
        assert(response['build_success'] == -2)
        # successful build
        corner1 = board.corners.get(yindex=3, xindex=4)
        corner2 = board.corners.get(yindex=2, xindex=3)
        build_attempt(board, corner1.yindex, corner1.xindex, response)
        assert(response['build_success'] == 1)
        # already built
        corner1.building = 1
        build_attempt(board, corner1.yindex, corner1.xindex, response)
        assert(response['build_success'] == -1)
        # neighbor rule violation
        corner1.building = 0
        corner2.building = 1
        build_attempt(board, corner1.yindex, corner1.xindex, response)
        assert(response['build_success'] == -3)
        corner2.building = 0

        """harvest method tests"""
        board.corners.get(yindex=4, xindex=4).building = 1
        board.corners.get(yindex=6, xindex=4).building = 1
        board.corners.get(yindex=9, xindex=4).building = 1
        dice_value = 8
        gather_resources(board, player1, dice_value, response)
        assert(player1.brick == 2)
        dice_value = 9
        gather_resources(board, player1, dice_value, response)
        assert(player1.grain == 2)
        dice_value = 11
        gather_resources(board, player1, dice_value, response)
        assert(player1.lumber == 1)
        