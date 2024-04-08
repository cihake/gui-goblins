from django.db import models
"""
A tile indicates resources, can be used for maritime trade, and may house the robber
"""
class Tile(models.Model):
    yindex = models.IntegerField()
    xindex = models.IntegerField()
    terrain = models.CharField(max_length=100)