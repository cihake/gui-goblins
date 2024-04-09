from django.db import models
import math
from .corner import Corner
from .tile import Tile
"""
The board that the game is played on. It has a 2D array both of corners and of tiles.
"""
class Board(models.Model):
    game_key = models.UUIDField(unique=True)
    corners = models.ManyToManyField('Corner', related_name='board')
    tiles = models.ManyToManyField('Tile', related_name='board')

    """Initialization; takes the game_key and coordinates"""
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
    
    """Get corner neighbors of corners; also checks for bounds"""
    def get_neighbor_corners(self, corner):
        y = corner.yindex
        x = corner.xindex
        corner_model = self.corners.through._meta.get_field('corner').remote_field.model
        corners = corner_model.objects.filter(board=self)  # Query all corner objects related to this board
        ymax = corners.aggregate(max_y=models.Max('yindex'))['max_y']
        xmax = corners.aggregate(max_x=models.Max('xindex'))['max_x']
        neighbors = []
        # All have these neighbors.
        if y > 0: neighbors.append(corners.filter(yindex=y-1, xindex=x).first())
        if y < ymax: neighbors.append(corners.filter(yindex=y+1, xindex=x).first())
        # Determine the unique neighbor
        if y % 4 == 0 and y < ymax and x > 0:
            neighbors.append(corners.filter(yindex=y+1, xindex=x-1).first())
        elif y % 4 == 1 and y > 0 and x < ymax:
            neighbors.append(corners.filter(yindex=y-1, xindex=x+1).first())
        elif y % 4 == 2 and y < ymax and x < xmax:
            neighbors.append(corners.filter(yindex=y+1, xindex=x+1).first())
        elif y % 4 == 3 and y > 0 and x > 0:
            neighbors.append(corners.filter(yindex=y-1, xindex=x-1).first())
        
        return neighbors
    
    """Get tile neighbors of corners; also checks for bounds"""
    def get_neighbor_tiles(self, corner):
        yindex = corner.yindex
        x = corner.xindex
        tile_model = self.tiles.through._meta.get_field('tile').remote_field.model
        tiles = tile_model.objects.filter(board=self)  # Query all tile objects related to this board
        y = math.floor(yindex / 2)
        # There are four offsets, and each lacks one of them.
        neighbors = []
        neighbors.append(tiles.filter(yindex=y, xindex=x).first())
        if y > 0: neighbors.append(tiles.filter(yindex=y-1, xindex=x).first())
        if x > 0: neighbors.append(tiles.filter(yindex=y, xindex=x-1).first())
        if y > 0 and x > 0: neighbors.append(tiles.filter(yindex=y-1, xindex=x-1).first())
        if yindex % 4 == 0 and tiles.filter(yindex=y, xindex=x).first() in neighbors:
            neighbors.remove(tiles.filter(yindex=y, xindex=x).first())
        elif yindex % 4 == 1 and tiles.filter(yindex=y-1, xindex=x-1).first() in neighbors:
            neighbors.remove(tiles.filter(yindex=y-1, xindex=x-1).first())
        elif yindex % 4 == 2 and tiles.filter(yindex=y, xindex=x-1).first() in neighbors:
            neighbors.remove(tiles.filter(yindex=y, xindex=x-1).first())
        elif yindex % 4 == 3 and tiles.filter(yindex=y-1, xindex=x).first() in neighbors:
            neighbors.remove(tiles.filter(yindex=y-1, xindex=x).first())
        
        return neighbors
