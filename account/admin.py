from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Achievement


# Define custom admin class for the Account model, inheriting from UserAdmin.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'wins')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()  # Remove references to groups and user_permissions
    list_filter = ()  # Remove reference to groups

# Define custom admin class for the Achievement model.
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'requirements', 'coin_reward', 'score')
    search_fields = ('name',)
