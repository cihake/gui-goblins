from django.test import TestCase
import random, uuid
from .models.game import Game
from .models.player import Player
from .models.board import Board
from .models.corner import Corner
from .models.tile import Tile
from .view_methods import build_attempt, gather_resources, handle_setup, handle_road_build, can_afford

class CatanTests(TestCase):
    def test(self):
        dummy_key = uuid.uuid4()
        game = Game.objects.create(game_key=dummy_key, number_players=1)
        board = Board.initialize(dummy_key, False)
        player1 = Player.objects.create(game_key=dummy_key, ordinal=1, starting_settlements=2)
        
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
        response['announcement'] = ""

        # not touching land
        corner = board.corners.get(yindex=0, xindex=0)
        build_attempt(game, board, player1, corner.yindex, corner.xindex, response)
        self.assertTrue(response['build_success'] == -2)
        # successful build
        corner1 = board.corners.get(yindex=3, xindex=4, building=0)
        corner2 = board.corners.get(yindex=2, xindex=3, building=0)
        build_attempt(game, board, player1, corner1.yindex, corner1.xindex, response)
        self.assertTrue(response['build_success'] == 1)
        # already built
        corner1.building = 1; corner1.save()
        build_attempt(game, board, player1, corner1.yindex, corner1.xindex, response)
        self.assertTrue(response['build_success'] == -1)
        # neighbor rule violation
        corner1.building = 0; corner1.save(); corner2.building = 1; corner2.save()
        build_attempt(game, board, player1, corner1.yindex, corner1.xindex, response)
        self.assertTrue(response['build_success'] == -3)
        corner1.building = 0; corner1.save(); corner2.building = 0; corner2.save()

        """Game setup test (one player)"""
        # build mistake test
        response['announcement'] = ""; corner1.building = 1; corner1.save()
        handle_setup(game, board, player1, corner1.yindex, corner1.xindex, response)
        game.save(); player1.save()
        self.assertTrue(game.setup_flag == 1 and player1.starting_settlements == 2)
        # Successful build 1
        response['announcement'] = ""; corner1.building = 0; corner1.save()
        handle_setup(game, board, player1, corner1.yindex, corner1.xindex, response)
        game.save(); player1.save()
        self.assertTrue(game.setup_flag == 1 and player1.starting_settlements == 1)
        # Final successful build
        response['announcement'] = ""; corner1.building = 0; corner1.save()
        handle_setup(game, board, player1, corner1.yindex, corner1.xindex, response)
        game.save(); player1.save()
        self.assertTrue(game.setup_flag == 0 and player1.starting_settlements == 0)

        """Road building tests"""
        #handle_road_build (game, board, player1, yindex, xindex, response)
        response['announcement'] = ""
        for Corner in board.corners.all(): Corner.building = 0; Corner.save()
        
        # Over water tests
        game.build_flag = 2; game.save()
        handle_road_build (game, board, player1, 2, 1, response)
        self.assertTrue(response['build_success'] == -1)
        game.build_flag = 3; game.save()
        handle_road_build (game, board, player1, 2, 1, response)
        self.assertTrue(response['build_success'] == -1)

        # Road start tests
        game.build_flag = 2; game.save()
        corner = board.corners.get(yindex=7, xindex=2)
        # No building or road
        corner.building = 0; corner.save()
        handle_road_build (game, board, player1, corner.yindex, corner.xindex, response)
        self.assertTrue(response['build_success'] == -2)
        # Has building
        corner.building = 1; corner.save()
        handle_road_build (game, board, player1, corner.yindex, corner.xindex, response)
        self.assertTrue(response['build_success'] == 1)
        # Has road
        game.build_flag = 2; game.save()
        corner.building = 0; corner.roads += "1,"; corner.save
        handle_road_build (game, board, player1, corner.yindex, corner.xindex, response)
        self.assertTrue(response['build_success'] == 1)

        # Road end tests
        game.build_flag = 3; game.save()
        board.road_start = "7,2"; board.save()
        # Length test
        corner = board.corners.get(yindex=8, xindex=3)
        handle_road_build (game, board, player1, corner.yindex, corner.xindex, response)
        self.assertTrue(response['build_success'] == -3)
        # Successful build
        game.build_flag = 3; game.save()
        corner = board.corners.get(yindex=8, xindex=2)
        handle_road_build (game, board, player1, corner.yindex, corner.xindex, response)
        board.save()
        game.build_flag = 3; game.save()
        self.assertTrue(response['build_success'] == 1)
        # Overlap test
        handle_road_build (game, board, player1, corner.yindex, corner.xindex, response)
        print("Build success: " + str(response['build_success']))
        self.assertTrue(response['build_success'] == -4)

        """harvest method tests"""
        player1.wool = 0; player1.grain = 0; player1.lumber = 0; player1.brick = 0; player1. ore = 0; player1.save()
        corner1 = board.corners.get(yindex=4, xindex=4)
        corner1.building = 1; corner1.save()
        corner2 = board.corners.get(yindex=6, xindex=4)
        corner2.building = 1; corner2.save()
        corner3 = board.corners.get(yindex=9, xindex=4)
        corner3.building = 1; corner3.save()
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

        """afford method test"""
        # Cannot afford a settlement
        player1.wool=0; player1.grain=0; player1.lumber=0; player1.brick=0; player1.ore=0; player1.save()
        self.assertFalse(can_afford(player1, "build_settlement", response))
        # Can afford a settlement
        player1.wool=1; player1.grain=1; player1.lumber=1; player1.brick=1; player1.ore=0; player1.save()
        self.assertTrue(can_afford(player1, "build_settlement", response))
        # Cannot afford a road
        player1.wool=0; player1.grain=0; player1.lumber=0; player1.brick=0; player1.ore=0; player1.save()
        self.assertFalse(can_afford(player1, "build_road", response))
        # Can afford a road
        player1.wool=0; player1.grain=0; player1.lumber=1; player1.brick=1; player1.ore=0; player1.save()
        self.assertTrue(can_afford(player1, "build_road", response))