from django.db import models

"""
Game overhead. It stores the players, along with flags for turn progression
and multi-step interaction.
"""
class Game(models.Model):
    number_players = models.IntegerField()
    turn = models.IntegerField()


"""
The board that the game is played on. It has a 2D array both of corners and of tiles.
"""
class Board(models.Model):
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


"""
A corner can be built on, harvest and trade, and have roads between (with restrictions)
"""
class Corner(models.Model):
    yindex = models.IntegerField()
    xindex = models.IntegerField()
    building = models.IntegerField()

"""
A tile indicates resources, can be used for maritime trade, and may house the robber
"""
class Tile(models.Model):
    yindex = models.IntegerField()
    xindex = models.IntegerField()
    terrain = models.CharField(max_length=100)