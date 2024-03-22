"""
A player of the game.
They have a piece to represent them, with draw positions and index.
The draw positions can be used for animations.
They also have an ordinal (which player they are),
and whether or not their turn is skipped.
"""

class Player:
    skip = False
    space = 1

    def __init__(self, ypos=50, xpos=50, ordinal=0, name="null", image="null"):
        self.ypos = ypos
        self.xpos = xpos
        self.image = image
        self.ordinal = ordinal