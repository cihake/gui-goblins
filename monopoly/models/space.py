from django.db import models
"""
A space on the game board; each is unique
"""
class Space(models.Model):
    index = models.IntegerField(default=0)
    type = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)