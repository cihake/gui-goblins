from .corner import Corner
from .tile import Tile
import math
from dataclasses import dataclass

"""
The board that the game is played on. It has a 2D array both of corners and of tiles.
"""
@dataclass
class Board:
    corners: list
    tiles: list

    @staticmethod
    def initialize_corners(corner_rows, corner_cols):
        corners = []
        for y in range(corner_rows):
            row = []
            for x in range(corner_cols):
                row.append(Corner(y, x))
            corners.append(row)
        return corners
    
    @staticmethod
    def initialize_tiles(tile_rows, tile_cols):
        tiles = []
        for y in range(tile_rows):
            row = []
            for x in range(tile_cols):
                row.append(Tile(y, x, "null"))
            tiles.append(row)
        # Manually set the terrain
        terrain = [
            ["empty", "empty", "water", "water", "water", "empty", "empty"],
            ["empty", "water", "forest", "fields", "mountains", "water", "empty"],
            ["water", "hills", "pasture", "hills", "mountains", "water", "empty"],
            ["water", "mountains", "pasture", "desert", "fields", "pasture", "water"],
            ["water", "hills", "forest", "fields", "forest", "water", "empty"],
            ["empty", "water", "water", "water", "water", "empty", "empty"]
        ]
        
        tiles[3][3].terrain = "desert"
        return tiles
    
    @staticmethod
    def to_dict(corners, tiles):
        def filter_none(lst):
            return [elem.to_dict() for elem in lst if elem is not None]

        return {
            'corners': [filter_none(row) for row in corners],
            'tiles': [filter_none(row) for row in tiles],
        }

    @staticmethod
    def from_dict(data):
        def create_obj(obj_class, data_dict):
            return obj_class(**data_dict) if data_dict else None

        corners = [[create_obj(Corner, corner_data) for corner_data in row] for row in data['corners']]
        tiles = [[create_obj(Tile, tile_data) for tile_data in row] for row in data['tiles']]
        return Board(corners, tiles)
    
    
    """Get corner neighbors of corners; also checks for bounds"""
    def get_neighbor_corners(self, corner):
        y = corner.yindex
        x = corner.xindex
        corners = self.corners
        ymax = len(corners)
        xmax = len(corners[0])
        neighbors = []
        # All have these neighbors
        if y > 0: neighbors.append(corners[y-1][x])
        if y < ymax: neighbors.append(corners[y+1][x])
        # Determine the unique neighbor
        if y % 4 == 0 and y < ymax and x > 0:
            neighbors.append(corners[y+1][x-1])
        elif y % 4 == 1 and y > 0 and x < ymax:
            neighbors.append(corners[y-1][x+1])
        elif y % 4 == 2 and y < ymax and x < xmax:
            neighbors.append(corners[y+1][x+1])
        elif y % 4 == 3 and y > 0 and x > 0:
            neighbors.append(corners[y-1][x-1])
        
        return neighbors
    
    """Get tile neighbors of corners; also checks for bounds"""
    def get_neighbor_tiles(self, corner):
        yindex = corner.yindex
        x = corner.xindex
        tiles = self.tiles
        y = math.floor(yindex / 2) # Offsets calculated based on this
        # There are four offsets, and each lacks one of them
        neighbors = []
        neighbors.append(tiles[y][x])
        if y > 0: neighbors.append(tiles[y-1][x])
        if x > 0: neighbors.append(tiles[y][x-1])
        if y > 0 and x > 0: neighbors.append(tiles[y-1][x-1])
        if yindex % 4 == 0 and tiles[y][x] in neighbors:
            neighbors.remove(tiles[y][x])
        elif yindex % 4 == 1 and tiles[y-1][x-1] in neighbors:
            neighbors.remove(tiles[y-1][x-1])
        elif yindex % 4 == 2 and tiles[y][x-1] in neighbors:
            neighbors.remove(tiles[y][x-1])
        elif yindex % 4 == 3 and tiles[y-1][x] in neighbors:
            neighbors.remove(tiles[y-1][x])
        
        return neighbors
