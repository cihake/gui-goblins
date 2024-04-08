from django.db import models
"""
A corner can be built on, harvest and trade, and have roads between (with restrictions)
"""
class Corner(models.Model):
    yindex = models.IntegerField()
    xindex = models.IntegerField()
    building = models.IntegerField()
