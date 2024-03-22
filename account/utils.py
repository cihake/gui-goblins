from django.dispatch import receiver
from django.db.models.signals import post_save
#Function for adding coins after winning a game. 
def add_coins(user, coins):
    from .models import Coin
    coin = Coin.objects.get_or_create(user=user)[0]
    coin.amount += coins
    coin.save()

def add_score(user, score):
    from .models import Leaderboard
    leaderboard, _ = Leaderboard.objects.get_or_create(user=user)
    leaderboard.score += coins
    leaderboard.save()

