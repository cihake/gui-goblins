from django.db import models
"""
A corner can be built on, harvest and trade, and have roads between (with restrictions).
"player" refers to who built/upgraded the settlement while "roads" is a list of those players
whose roads connect to the corner (up to 3).
"""
class Corner(models.Model):
    yindex = models.IntegerField(default=0)
    xindex = models.IntegerField(default=0)
    building = models.IntegerField(default=0)
    player = models.IntegerField(default=0)
    roads = models.CharField(max_length=100, null=True)

    def __str__(self):
        y = str(self.yindex) + ","
        x = str(self.xindex) + " "
        building = "Building:" + str(self.building) + " - "
        player = "Player:" + str(self.player) + " - "
        roads = "Roads:" + self.roads + " - "
        return "Corner:" + y + x + building + player + roads