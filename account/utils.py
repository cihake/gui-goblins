from django.dispatch import receiver  # Importing the receiver decorator for signal handling.
from django.db.models.signals import post_save  # Importing the post_save signal for post-save operations.

# Function for adding coins after winning a game.
def add_coins(user, coins):
    from .models import Coin  # Importing the Coin model from the current app's models.
    coin = Coin.objects.get_or_create(user=user)[0]  # Getting or creating a Coin object for the user.
    coin.amount += coins  # Adding coins to the user's balance.
    coin.save()  # Saving the updated Coin object.

# Function for adding score after winning a game.
def add_score(user, score):
    from .models import Leaderboard  # Importing the Leaderboard model from the current app's models.
    leaderboard, _ = Leaderboard.objects.get_or_create(user=user)  # Getting or creating a Leaderboard object for the user.
    leaderboard.score += score  # Adding score to the user's leaderboard.
    leaderboard.save()  # Saving the updated Leaderboard object.
