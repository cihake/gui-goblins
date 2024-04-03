from django.db import models  # Importing the models module from Django for defining database models.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager  # Importing base classes for custom user model.
from .utils import add_coins  # Importing utility function add_coins from local module.

# Custom manager for managing user accounts.
class MyAccountManager(BaseUserManager):
    # Method to create a regular user.
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

    # Method to create a superuser.
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

# Custom user model for user accounts.
class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)  # Email field for user's email address.
    username = models.CharField(max_length=30, unique=True)  # Field for user's username.
    wins = models.IntegerField(default=0)
    date_joined = models.DateTimeField(verbose_name='date joined',auto_now_add=True)  # Field to store user's registration date.
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)  # Field to store user's last login date.
    is_admin = models.BooleanField(default=False)  # Flag indicating if the user is an admin.
    is_active = models.BooleanField(default=True)  # Flag indicating if the user account is active.
    is_staff = models.BooleanField(default=False)  # Flag indicating if the user is staff.
    is_superuser = models.BooleanField(default=False)  # Flag indicating if the user is a superuser.
    USERNAME_FIELD = 'email'  # Field used for authentication (email).
    REQUIRED_FIELDS = ['username']  # Fields required for user creation.
    from django.db import transaction

    objects = MyAccountManager()  # Custom manager for user accounts.

    def __str__(self):
        return self.email  # String representation of the user object.

    def has_perm(self, perm, obj=None):
        return self.is_admin  # Method to check if user has specific permission.

    def has_module_perms(self, app_label):
        return True  # Method to check if user has permission to access a specific app/module.

# Model to store user's coins.
class Coin(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)  # Relationship with user account.
    amount = models.IntegerField(default=0)  # Field to store the amount of coins.

    def __str__(self):
        return f"{self.user.username}'s Coins"  # String representation of the user's coins.

# Model to define achievements for users.
class Achievement(models.Model):
    name = models.CharField(max_length=100)  # Field for achievement name.
    description = models.TextField()  # Field for achievement description.
    requirements = models.CharField(max_length=100)  # Field for achievement requirements.
    coin_reward = models.IntegerField(default=0)  # Field for coin reward for achieving.
    score = models.IntegerField(default=0)  # Field for achievement score.

    def __str__(self):
        return self.name  # String representation of the achievement.

# Model to link users with their earned achievements.
class UserAchievement(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)  # Relationship with user account.
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)  # Relationship with achievement.
    earned_at = models.DateTimeField(auto_now_add=True)  # Field to store the time when achievement was earned.

    def __str__(self):
        return f"{self.user.username}: {self.achievement.name}"  # String representation of user's earned achievements.

# Model to store user scores for leaderboard.
class Leaderboard(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)  # Relationship with user account.
    score = models.IntegerField(default=0)  # Field to store user's score.
    wins = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}: {self.score}"  # String representation of user's score in leaderboard.
