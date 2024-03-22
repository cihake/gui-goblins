"""
The board that the game is played on.
It has an array of spaces, with various properties.
"""

from space import Space

class Board:
    colors = ["red", "purple", "yellow", "blue", "orange", "green"]
    spaces = []
    """ypositions = []
    xpositions = []"""

    """
    Draw positions and scale are externally defined
    Spaces are added in sequence, with individual values and possibly a skip space
    """
    def __init__(self, ypos=50, xpos=50, scale=1):
        self.ypos = ypos
        self.xpos = xpos
        self.scale = scale
        
        # add a blank space at the 0 position
        self.spaces.append(Space(0, 0, "null", "null", False))
        
        pattern = 0 # to loop through the list of colors

        for i in range(1, 128):
            space_value = "null"
            space_skip = False
            space_ypos = 0
            space_xpos = 0
            
            # define the space color, in pattern
            space_color = self.colors[pattern]
            pattern += 1
            if (pattern==6): pattern = 0 # loop back

            # define the special spaces
            if (i==70 or i==106): space_skip = True
            elif (i==9): space_value = "entrance1"
            elif (i==20): space_value = "entrance2"
            elif (i==34): space_value = "exit2"
            elif (i==35): space_value = "peppermint"
            elif (i==45): space_value = "exit1"
            elif (i==51): space_value = "peanut"
            elif (i==81): space_value = "lollipop"
            elif (i==115): space_value = "frosted"
            else:
                # define the space color, in pattern
                spaec_value = self.colors[pattern]
                pattern += 1
                if (pattern==6): pattern = 0 # loop back

            # define the positions of the spaces
            space_ypos = self.ypos
            space_xpos = self.xpos
            """Replace with this once the positions are known
            space_ypos = self.ypos + self.ypositions[i-1] * self.scale
            space_xpos = self.xpos + self.xpositions[i-1] * self.scale"""

            # add the defined space
            self.spaces.append(Space(space_ypos, space_xpos, i,
                                     space_value, space_skip))
            

    """Update the draw positions of each of the board's spaces"""
    def update(self):
        for Space in self.spaces:
            Space.ypos = self.ypos
            Space.xpos = self.xpos
            """Replace with this once the positions are known
            Space.ypos = self.ypos + self.ypositions[i] * self.scale
            Space.xpos = self.xpos + self.xpositions[i] * self.scale"""