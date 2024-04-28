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
    road_start = models.CharField(max_length=100, null=True)
    existing_roads = models.CharField(max_length=10000, null=True)

    """Initialization; takes the game_key and coordinates"""
    @classmethod
    def initialize(cls, game_key):
        board = cls.objects.create(game_key=game_key)
        board.existing_roads = ""

        corners = []
        for y in range(16):
            for x in range(8):
                corner = Corner(yindex=y, xindex=x, building=0, player=0, roads="")
                corners.append(corner)
        Corner.objects.bulk_create(corners)
        board.corners.add(*corners)
        
        tile_terrain = [
            ["empty", "empty", "water", "water", "water", "empty", "empty"],
            ["empty", "water", "forest", "fields", "mountains", "water", "empty"],
            ["water", "hills", "pasture", "hills", "mountains", "water", "empty"],
            ["water", "mountains", "pasture", "desert", "fields", "pasture", "water"],
            ["water", "hills", "forest", "fields", "forest", "water", "empty"],
            ["empty", "water", "fields", "forest", "pasture", "water", "empty"],
            ["empty", "water", "water", "water", "water", "empty", "empty"]
        ]
        tile_dice = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 6, 5, 9, 0, 0],
            [0, 4, 3, 8, 10, 0, 0],
            [0, 6, 5, 0, 9, 12, 0],
            [0, 3, 2, 10, 11, 0, 0],
            [0, 0, 11, 4, 8, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
        tiles = []
        for y in range(7):
            for x in range(7):
                terrain = tile_terrain[y][x]
                dice = tile_dice[y][x]
                tile = Tile(yindex=y, xindex=x, terrain=terrain, dice=dice)
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
        # Get an intermediate "corners" model
        corner_model = self.corners.through._meta.get_field('corner').remote_field.model
        corners = corner_model.objects.filter(board=self)  # Query all corner objects related to this board
        neighbors = []
        # All have these neighbors.
        if corners.filter(yindex=y-1, xindex=x).exists():
            neighbors.append(corners.get(yindex=y-1, xindex=x))
        if corners.filter(yindex=y+1, xindex=x).exists():
            neighbors.append(corners.get(yindex=y+1, xindex=x))
        # Determine the unique neighbor
        if y % 4 == 0 and corners.filter(yindex=y+1, xindex=x-1).exists():
            neighbors.append(corners.get(yindex=y+1, xindex=x-1))
        elif y % 4 == 1 and corners.filter(yindex=y-1, xindex=x+1).exists():
            neighbors.append(corners.get(yindex=y-1, xindex=x+1))
        elif y % 4 == 2 and corners.filter(yindex=y+1, xindex=x+1).exists():
            neighbors.append(corners.get(yindex=y+1, xindex=x+1))
        elif y % 4 == 3 and corners.filter(yindex=y-1, xindex=x-1).exists():
            neighbors.append(corners.get(yindex=y-1, xindex=x-1))

        self.print_neighbor_corners(neighbors)
        
        return neighbors
    
    """Get tile neighbors of corners; also checks for bounds"""
    def get_neighbor_tiles(self, corner):
        yindex = corner.yindex
        x = corner.xindex
        # Get an intermediate "tiles" model
        tile_model = self.tiles.through._meta.get_field('tile').remote_field.model
        tiles = tile_model.objects.filter(board=self)  # Query all tile objects related to this board
        y = math.floor(yindex / 2)
        # There are four offsets, and each lacks one of them.
        neighbors = []
        if yindex % 4 != 0 and tiles.filter(yindex=y, xindex=x).exists():
            neighbors.append(tiles.get(yindex=y, xindex=x))
        if yindex % 4 != 1 and tiles.filter(yindex=y-1, xindex=x-1).exists():
            neighbors.append(tiles.get(yindex=y-1, xindex=x-1))
        if yindex % 4 != 2 and tiles.filter(yindex=y, xindex=x-1).exists():
            neighbors.append(tiles.get(yindex=y, xindex=x-1))
        if yindex % 4 != 3 and tiles.filter(yindex=y-1, xindex=x).exists():
            neighbors.append(tiles.get(yindex=y-1, xindex=x))

        self.print_neighbor_tiles(neighbors)
        
        return neighbors
    
    """Print check for the neighbor corners method"""
    def print_neighbor_corners(self, neighbor_corners):
        output = ""
        for Corner in neighbor_corners:
            output += Corner.__str__()
        print(output)
    
    """Print check for the nieghbor tiles method"""
    def print_neighbor_tiles(self, neighbor_tiles):
        output = ""
        for Tile in neighbor_tiles:
            output += Tile.__str__()
        print(output)