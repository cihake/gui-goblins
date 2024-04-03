# Django's authenticated admin framework. 
from django.contrib import admin
# Imports the pre-defined class, UserAdmin, which offers an administrative interface for managing user accounts.
from django.contrib.auth.admin import UserAdmin
# Imports the Account and Achievement models.
from .models import Account, Achievement

# Define custom admin class for the Account model, inheriting from UserAdmin.
class AccountAdmin(UserAdmin):
    # Specify fields to be displayed in the list view of the admin panel.
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'wins')
    # Enable searching by email and username in the admin panel
    search_fields = ('email', 'username',)
    # Specify fields to be displayed as read-only in the admin panel
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
# Define custom admin class for the Achievement model.
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'requirements', 'coin_reward', 'score')
    search_fields = ('name',)

# Register the Achievement model with its custom admin class.
admin.site.register(Achievement, AchievementAdmin)

# Register the admin class for the Account model
admin.site.register(Account, AccountAdmin)


