"""
A corner can be built on, harvest and trade, and have roads between (with restrictions)
"""
class Corner:
    def __init__(self, yindex, xindex):
        self.yindex = yindex
        self.xindex = xindex
        self.building = 0

    """to_dict is used for session variable saving"""
    def to_dict(self):
        return {
            'yindex': self.yindex,
            'xindex': self.xindex,
            'building': self.building,
        }