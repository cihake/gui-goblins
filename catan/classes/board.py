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
        # Manually set terrain for a specific tile
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
    
    """Get corner neighbors of corners"""
    def get_neighbor_corners(self, corner):
        y = corner.yindex
        x = corner.xindex
        corners = self.corners
        # All have these neighbors
        neighbor1 = corners[y-1][x]
        neighbor2 = corners[y+1][x]
        # Determine the unique neighbor
        if y % 4 == 0:
            neighbor3 = corners[y+1][x-1]
        elif y % 4 == 1:
            neighbor3 = corners[y-1][x+1]
        elif y % 4 == 2:
            neighbor3 = corners[y+1][x+1]
        elif y % 4 == 3:
            neighbor3 = corners[y-1][x-1]
        
        return [neighbor1, neighbor2, neighbor3]
    
    """Get tile neighbors of corners"""
    def get_neighbor_tiles(self, corner):
        yindex = corner.yindex
        x = corner.xindex
        tiles = self.tiles
        y = math.floor(yindex / 2) # Offsets calculated based on this
        # There are four offsets, and each lacks one of them
        neighbors = [tiles[y-1][x-1], tiles[y-1][x], tiles[y][x-1], tiles[y][x]]
        if yindex % 4 == 0:
            neighbors.remove(tiles[y][x])
        elif yindex % 4 == 1:
            neighbors.remove(tiles[y-1][x-1])
        elif yindex % 4 == 2:
            neighbors.remove(tiles[y][x-1])
        elif yindex % 4 == 3:
            neighbors.remove(tiles[y-1][x])
        
        return neighbors
