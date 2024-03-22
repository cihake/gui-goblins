"""
Spaces on the board for people to land on.
Their index is given by their position on an ArrayList.
Note that "pink" is a color, not a special.
"""
class Space:
    def __init__(self, ypos, xpos, index, color, special):
        self.ypos = ypos
        self.xpos = xpos
        self.index = index
        self.color = color
        self.special = special