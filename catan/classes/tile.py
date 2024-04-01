class Tile:
    def __init__(self, yindex, xindex, terrain):
        self.yindex = yindex
        self.xindex = xindex
        self.terrain = terrain
    
    """to_dict is used for session variable saving"""
    def to_dict(self):
        return {
            'yindex': self.yindex,
            'xindex': self.xindex,
            'terrain': self.terrain,
        }