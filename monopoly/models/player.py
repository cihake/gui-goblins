from django.db import models
"""
A player of the game. They have an ordinal (which player they are),
the space that their piece is on, and a money total.
"""
class Player(models.Model):
    game_key = models.UUIDField(unique=True, null=True)
    ordinal = models.IntegerField(default=-1)
    space = models.IntegerField(default=0)
    money = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        # Initialize money balance to $1500 when a new player is created
        if not self.pk:
            self.money = 1500
        super().save(*args, **kwargs)    