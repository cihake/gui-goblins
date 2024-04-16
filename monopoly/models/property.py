from django.db import models
"""
A property card. It has a title, a group, a list of prices, and a list of rents.
Properties can be in the deck (0), or assigned to a player (ordinal-based).
Prices are buy, build, mortgage; rents are based on build amount
"""
class Property(models.Model):
    player = models.IntegerField(default=0)
    index = models.IntegerField(default=0)
    group = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)
    prices = models.CharField(max_length=100, null=True)
    rents = models.CharField(max_length=100, null=True)
