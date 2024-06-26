from django.db import models
"""
A tile indicates resources, can be used for maritime trade, and may house the robber
"""
class Tile(models.Model):
    yindex = models.IntegerField(default=0)
    xindex = models.IntegerField(default=0)
    terrain = models.CharField(max_length=100)
    dice = models.IntegerField(default=0)

    def __str__(self):
        y = str(self.yindex) + ","
        x = str(self.xindex) + " "
        terrain = "Terrain:" + self.terrain + ", "
        dice = "Dice:" + str(self.dice) + " - "
        return "Tile:" + y + x + terrain + dice