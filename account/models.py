from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .utils import add_coins

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )

        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label
):
        return True

# Defines the Coin model for use in the database.
class Coin(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

# toString method that returns a string representation of the user's Coins. 
    def __str__(self):
        return f"{self.user.username}'s Coins"

# Model to define achievements for users. 
class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.CharField(max_length=100)
    coin_reward = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.name
# Model to link users with their earned achievements. 
class UserAchievement(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.achievement.name}"

class Leaderboard(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}: {self.score}"