from .corner import Corner
from .tile import Tile

"""
The board that the game is played on. It has a 2D array both of corners and of tiles.
"""
class Board:
    def __init__(self, corner_rows, corner_cols, tile_rows, tile_cols):
        # Initialize grid of corners
        self.corners = [[None] * corner_cols for _ in range(corner_rows)]
        for y in range(corner_rows):
            for x in range(corner_cols):
                self.corners[y][x] = Corner(y, x)
        # Initialize grid of tiles
        self.tiles = [[None] * tile_cols for _ in range(tile_rows)]
        for y in range(tile_rows):
            for x in range(tile_cols):
                self.tiles[y][x] = Tile(y, x, "empty")
    
    """to_dict is used for session variable saving"""
    def to_dict(self):
        return {
            'corners': [[corner.to_dict() for corner in row] for row in self.corners],
            'tiles': [[tile.to_dict() for tile in row] for row in self.tiles],
        }