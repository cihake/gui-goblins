from django.test import TestCase
import random, uuid
from .models.game import Game
from .models.player import Player
from .models.board import Board
from .models.corner import Corner
from .models.tile import Tile
from .view_methods import build_attempt, gather_resources, handle_setup, handle_road_build, can_afford, move_attempt, steal_resource

class CatanTests(TestCase):
    def test(self):
        dummy_key = uuid.uuid4()
        game = Game.initialize(dummy_key, 3, 2)
        board = Board.initialize(dummy_key, False)
        player1 = game.players.get(ordinal=1)
        
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
        
        tile = board.tiles.get(yindex=3, xindex=3)
        surrounding_corners = board.get_surrounding_corners(tile)
        for Corner in surrounding_corners:
            self.assertTrue(Corner.xindex == 3 and Corner.yindex == 6 or
                            Corner.xindex == 4 and Corner.yindex == 7 or
                            Corner.xindex == 4 and Corner.yindex == 8 or
                            Corner.xindex == 3 and Corner.yindex == 9 or
                            Corner.xindex == 3 and Corner.yindex == 8 or
                            Corner.xindex == 3 and Corner.yindex == 7)
        
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

        """Game setup test (Two players)"""
        # build mistake test
        response['announcement'] = ""; corner1.building = 1; corner1.save()
        player = game.players.get(ordinal=game.turn)
        handle_setup(game, board, player, corner1.yindex, corner1.xindex, response)
        game.save()
        self.assertTrue(game.setup_flag == 1 and game.turn == 1 and player.starting_settlements == 2)
        # Successful build 1; next player
        response['announcement'] = ""; corner1.building = 0; corner1.save()
        player = game.players.get(ordinal=game.turn)
        handle_setup(game, board, player, corner1.yindex, corner1.xindex, response)
        game.save()
        self.assertTrue(game.setup_flag == 1 and game.turn == 2 and player.starting_settlements == 1)
        # Successful build 2; next player
        response['announcement'] = ""; corner1.building = 0; corner1.save()
        player = game.players.get(ordinal=game.turn)
        handle_setup(game, board, player, corner1.yindex, corner1.xindex, response)
        game.save()
        self.assertTrue(game.setup_flag == 1 and game.turn == 3 and player.starting_settlements == 1)
        # Successful build 3; loop back
        response['announcement'] = ""; corner1.building = 0; corner1.save()
        player = game.players.get(ordinal=game.turn)
        handle_setup(game, board, player, corner1.yindex, corner1.xindex, response)
        game.save()
        self.assertTrue(game.setup_flag == 1 and game.turn == 1 and player.starting_settlements == 1)
        # Successful build 4; next player
        response['announcement'] = ""; corner1.building = 0; corner1.save()
        player = game.players.get(ordinal=game.turn)
        handle_setup(game, board, player, corner1.yindex, corner1.xindex, response)
        game.save()
        self.assertTrue(game.setup_flag == 1 and game.turn == 2 and player.starting_settlements == 0)
        # Successful build 5; next player
        response['announcement'] = ""; corner1.building = 0; corner1.save()
        player = game.players.get(ordinal=game.turn)
        handle_setup(game, board, player, corner1.yindex, corner1.xindex, response)
        game.save()
        self.assertTrue(game.setup_flag == 1 and game.turn == 3 and player.starting_settlements == 0)
        # Final successful build
        response['announcement'] = ""; corner1.building = 0; corner1.save()
        player = game.players.get(ordinal=game.turn)
        handle_setup(game, board, player, corner1.yindex, corner1.xindex, response)
        game.save()
        self.assertTrue(game.setup_flag == 0 and game.turn == 1 and player.starting_settlements == 0)

        """Road building tests"""
        #handle_road_build (game, board, player, yindex, xindex, response)
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
        # Has building and matches player
        corner.building = 1; corner.player = 1; corner.save()
        handle_road_build (game, board, player1, corner.yindex, corner.xindex, response)
        self.assertTrue(response['build_success'] == 1)
        # Has a road, but not the right one
        player2 = game.players.get(ordinal=2)
        game.build_flag = 2; game.save()
        corner.building = 0; corner.roads = "1"; corner.save()
        handle_road_build (game, board, player2, corner.yindex, corner.xindex, response)
        self.assertTrue(response['build_success'] == -2)
        # Has the right road
        game.build_flag = 2; game.save()
        corner.building = 0; corner.roads = "1"; corner.save()
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
        corner1.building = 1; corner1.player = 1; corner1.save()
        corner2 = board.corners.get(yindex=6, xindex=4)
        corner2.building = 1; corner2.player = 1;  corner2.save()
        corner3 = board.corners.get(yindex=9, xindex=4)
        corner3.building = 1; corner3.player = 1;  corner3.save()
        dice_value = 8
        gather_resources(game, board, dice_value, response)
        player1 = game.players.get(ordinal=1)
        self.assertTrue(player1.brick == 2)
        dice_value = 9
        gather_resources(game, board, dice_value, response)
        player1 = game.players.get(ordinal=1)
        self.assertTrue(player1.grain == 2)
        dice_value = 11
        gather_resources(game, board, dice_value, response)
        player1 = game.players.get(ordinal=1)
        self.assertTrue(player1.lumber == 1)
        dice_value = 11 # City increased gathering
        corner3.building = 2; corner3.save()
        gather_resources(game, board, dice_value, response)
        player1 = game.players.get(ordinal=1)
        self.assertTrue(player1.lumber == 3)
        dice_value = 11 # Other player, do not gather
        corner3.player = 2; corner3.save()
        gather_resources(game, board, dice_value, response)
        player1 = game.players.get(ordinal=1)
        self.assertTrue(player1.lumber == 3)
        dice_value = 11 # Other player, do not gather
        corner3.player = 2; corner3.save()
        gather_resources(game, board, dice_value, response)
        player1 = game.players.get(ordinal=1)
        self.assertTrue(player1.lumber == 3)
        # Robber test; do not gather
        dice_value = 11
        board.robber_space = "4,4"; board.save()
        corner3.player = 1; corner3.save()
        gather_resources(game, board, dice_value, response)
        player1 = game.players.get(ordinal=1)
        self.assertTrue(player1.lumber == 3)

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
        # Cannot afford a city
        player1.wool=0; player1.grain=0; player1.lumber=0; player1.brick=0; player1.ore=0; player1.save()
        self.assertFalse(can_afford(player1, "build_city", response))
        # Can afford a city
        player1.wool=0; player1.grain=2; player1.lumber=0; player1.brick=0; player1.ore=3; player1.save()
        self.assertTrue(can_afford(player1, "build_city", response))

        """Robber move tests"""
        response['announcement'] = ""
        board.robber_space = "3,3"; board.save()
        # Not a land tile
        move_attempt(game, board, 0, 0, response)
        self.assertTrue(response['move_success'] == -1)
        # Same space
        move_attempt(game, board, 3, 3, response)
        board.save()
        self.assertTrue(response['move_success'] == -2)
        # Successful move
        move_attempt(game, board, 4, 4, response)
        self.assertTrue(response['move_success'] == 1)

        """Steal method tests"""
        corner1 = board.corners.get(yindex=6, xindex=3)
        corner1.building = 1; corner1.player = 1; corner1.save()
        corner2 = board.corners.get(yindex=9, xindex=3)
        corner2.building = 1; corner2.player = 2; corner2.save()
        # No resource stolen
        player1.wool=0; player1.grain=0; player1.lumber=0; player1.brick=0; player1.ore=0; player1.save()
        player2.wool=0; player2.grain=0; player2.lumber=0; player2.brick=0; player2.ore=0; player2.save()
        steal_resource(game, board, player1, 3, 3, response)
        player1 = game.players.get(ordinal=1)
        player2 = game.players.get(ordinal=2)
        self.assertTrue(player1.wool == 0 and player1.grain == 0 and player1.lumber == 0 and player1.brick == 0 and player1.ore == 0 and
                    player2.wool == 0 and player2.grain == 0 and player2.lumber == 0 and player2.brick == 0 and player2.ore == 0)
        # Resource stolen
        player1.wool=0; player1.grain=0; player1.lumber=0; player1.brick=0; player1.ore=0; player1.save()
        player2.wool=1; player2.grain=0; player2.lumber=0; player2.brick=0; player2.ore=0; player2.save()
        steal_resource(game, board, player1, 3, 3, response)
        player1 = game.players.get(ordinal=1)
        player2 = game.players.get(ordinal=2)
        self.assertTrue(player1.wool == 1 and player2.wool == 0)
        # Choice of resource stolen
        player1.wool=0; player1.grain=0; player1.lumber=0; player1.brick=0; player1.ore=0; player1.save()
        player2.wool=0; player2.grain=2; player2.lumber=0; player2.brick=0; player2.ore=0; player2.save()
        steal_resource(game, board, player1, 3, 3, response)
        player1 = game.players.get(ordinal=1)
        player2 = game.players.get(ordinal=2)
        self.assertTrue(player1.wool == 1 and player2.wool == 0 or player1.grain == 1 and player2.grain == 1)