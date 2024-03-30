from django.db import models


class Game(models.Model):
    victory = models.IntegerField()

    def to_dict(self):
        return {
            'victory': self.victory,
        }

"""
A player of the game. They have an ordinal (which player they are),
the space that their piece is on, and whether their turn is skipped.
"""
class Player(models.Model):
    ordinal = models.IntegerField()
    space = models.IntegerField()
    skip = models.BooleanField()

    def to_dict(self):
        return {
            'ordinal': self.ordinal,
            'space': self.space,
            'skip': self.skip
        }