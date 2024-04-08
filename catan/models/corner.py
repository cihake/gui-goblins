from django.db import models
"""
A corner can be built on, harvest and trade, and have roads between (with restrictions)
"""
class Corner(models.Model):
    yindex = models.IntegerField(default=0)
    xindex = models.IntegerField(default=0)
    player = models.IntegerField(default=0)
    building = models.IntegerField(default=0)
