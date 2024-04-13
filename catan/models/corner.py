from django.db import models
"""
A corner can be built on, harvest and trade, and have roads between (with restrictions)
"""
class Corner(models.Model):
    yindex = models.IntegerField(default=0)
    xindex = models.IntegerField(default=0)
    building = models.IntegerField(default=0)

    def __str__(self):
        y = str(self.yindex) + ","
        x = str(self.xindex) + " "
        building = "Building:" + str(self.building) + " - "
        return "Corner:" + y + x + building