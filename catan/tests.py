from django.test import TestCase
import random, uuid
from .models.game import Game
from .models.player import Player
from .models.board import Board
from .models.corner import Corner
from .models.tile import Tile
from .view_methods import build_attempt, gather_resources

class CatanTests(TestCase):
    def test(self):
        dummy_key = uuid.uuid4()
        game = Game.objects.create(game_key=dummy_key)
        board = Board.initialize(dummy_key)
        player1 = Player.objects.create(game_key=dummy_key, ordinal=1)
        
        """neighbor method tests"""
        corner = board.corners.get(yindex=3, xindex=4, building=0)
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
        
        corner = board.corners.get(yindex=4, xindex=3, building=0)
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
            
        corner = board.corners.get(yindex=5, xindex=4, building=0)
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
            
        corner = board.corners.get(yindex=6, xindex=3, building=0)
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
            
        corner = board.corners.get(yindex=8, xindex=0, building=0)
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
        self.assertTrue(response['build_success'] == -2)
        # successful build
        corner1 = board.corners.get(yindex=3, xindex=4, building=0)
        corner2 = board.corners.get(yindex=2, xindex=3, building=0)
        build_attempt(board, corner1.yindex, corner1.xindex, response)
        self.assertTrue(response['build_success'] == 1)
        # already built
        corner1.building = 1
        corner1.save()
        build_attempt(board, corner1.yindex, corner1.xindex, response)
        self.assertTrue(response['build_success'] == -1)
        # neighbor rule violation
        corner1.building = 0
        corner1.save()
        corner2.building = 1
        corner2.save()
        build_attempt(board, corner1.yindex, corner1.xindex, response)
        print("Build success: " + str(response['build_success']))
        self.assertTrue(response['build_success'] == -3)
        corner1.building = 0
        corner1.save()
        corner2.building = 0
        corner2.save()

        """harvest method tests"""
        corner1 = board.corners.get(yindex=4, xindex=4)
        corner1.building = 1
        corner1.save()
        corner2 = board.corners.get(yindex=6, xindex=4)
        corner2.building = 1
        corner2.save()
        corner3 = board.corners.get(yindex=9, xindex=4)
        corner3.building = 1
        corner3.save()
        dice_value = 8
        gather_resources(board, player1, dice_value, response)
        player1.save()
        self.assertTrue(player1.brick == 2)
        dice_value = 9
        gather_resources(board, player1, dice_value, response)
        player1.save()
        self.assertTrue(player1.grain == 2)
        dice_value = 11
        gather_resources(board, player1, dice_value, response)
        player1.save()
        self.assertTrue(player1.lumber == 1)
        