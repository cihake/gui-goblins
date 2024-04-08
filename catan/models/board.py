from django.db import models
from .corner import Corner
from .tile import Tile
"""
The board that the game is played on. It has a 2D array both of corners and of tiles.
"""
class Board(models.Model):
    game_key = models.UUIDField(unique=True)
    corners = models.ManyToManyField('Corner', related_name='board')
    tiles = models.ManyToManyField('Tile', related_name='board')

    @classmethod
    def initialize(cls, game_key, corner_rows, corner_cols, tile_rows, tile_cols):
        board = cls.objects.create(game_key=game_key)

        corners = []
        for y in range(corner_rows):
            for x in range(corner_cols):
                corner = Corner(yindex=y, xindex=x, building=0)
                corners.append(corner)
        Corner.objects.bulk_create(corners)
        board.corners.add(*corners)

        tiles = []
        for y in range(tile_rows):
            for x in range(tile_cols):
                terrain = "null"  # Set default terrain
                tile = Tile(yindex=y, xindex=x, terrain=terrain)
                tiles.append(tile)
        Tile.objects.bulk_create(tiles)
        board.tiles.add(*tiles)

        return board
    
    # Method to get corner at given coordinates
    def get_corner(self, y, x):
        return self.corners.get(yindex=y, xindex=x)

    # Method to get tile at given coordinates
    def get_tile(self, y, x):
        return self.tiles.get(yindex=y, xindex=x)

    # Method to update corner attribute at given coordinates
    def update_corner(self, y, x, attributes):
        corner = self.corners.get(yindex=y, xindex=x)
        if corner:
            for attr_name, attr_value in attributes.items():
                setattr(corner, attr_name, attr_value)
            corner.save()  # Save the corner after updating

    # Method to update tile attribute at given coordinates
    def update_tile(self, y, x, attributes):
        tile = self.tiles.get(yindex=y, xindex=x)
        if tile:
            for attr_name, attr_value in attributes.items():
                setattr(tile, attr_name, attr_value)
            tile.save()  # Save the tile after updating