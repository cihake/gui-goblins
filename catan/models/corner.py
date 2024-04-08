from django.db import models
"""
A corner can be built on, harvest and trade, and have roads between (with restrictions)
"""
class Corner(models.Model):
    game_key = models.UUIDField(primary_key=True)
    yindex = models.IntegerField()
    xindex = models.IntegerField()
    building = models.IntegerField()