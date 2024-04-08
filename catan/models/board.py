from django.db import models
from .corner import Corner
from .tile import Tile
"""
The board that the game is played on. It has a 2D array both of corners and of tiles.
"""
class Board(models.Model):
    game_key = models.UUIDField(primary_key=True)
    corners = models.ManyToManyField('Corner', related_name='board')
    tiles = models.ManyToManyField('Tile', related_name='board')

    @classmethod
    def initialize(cls, corner_rows, corner_cols, tile_rows, tile_cols):
        board = cls.objects.create()

        # Create corners
        for y in range(corner_rows):
            for x in range(corner_cols):
                corner = Corner(yindex=y, xindex=x, building=0)
                corner.save()
                board.corners.add(corner)

        # Create tiles
        for y in range(tile_rows):
            for x in range(tile_cols):
                terrain = "null"  # Set default terrain
                tile = Tile(yindex=y, xindex=x, terrain=terrain)
                tile.save()
                board.tiles.add(tile)

        return board
    
    # Method to get corner at given coordinates
    def get_corner(self, y, x):
        return self.corners.filter(yindex=y, xindex=x).first()

    # Method to update corner attribute at given coordinates
    def update_corner(self, y, x, attributes):
        corner = self.get_corner_at(y, x)
        if corner:
            for attr_name, attr_value in attributes.items():
                setattr(corner, attr_name, attr_value)
            corner.save()

    # Method to get tile at given coordinates
    def get_tile(self, y, x):
        return self.tiles.filter(yindex=y, xindex=x).first()

    # Method to update tile attribute at given coordinates
    def update_tile(self, y, x, attributes):
        tile = self.get_tile_at(y, x)
        if tile:
            for attr_name, attr_value in attributes.items():
                setattr(tile, attr_name, attr_value)
            tile.save()