from django.db import models
"""
A player of the game. They have an ordinal (which player they are)
and a resource total.
"""
class Player(models.Model):
    ordinal = models.IntegerField(default=-1)
    starting_settlements = models.IntegerField(default=0)
    number_cities = models.IntegerField(default=0)
    wool = models.IntegerField(default=0)
    grain = models.IntegerField(default=0)
    lumber = models.IntegerField(default=0)
    brick = models.IntegerField(default=0)
    ore = models.IntegerField(default=0)

    def __str__(self):
        ordinal = "Player:" + str(self.ordinal) + ", "
        wool = "Wool:" + str(self.wool) + ", "
        grain = "Grain:" + str(self.grain) + ", "
        lumber = "Lumber:" + str(self.lumber) + ", "
        brick = "Brick:" + str(self.brick) + ", "
        ore = "Ore:" + str(self.ore) + ", "
        return ordinal + wool + grain + lumber + brick + ore