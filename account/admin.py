from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account
from .models import Achievement

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'requirements', 'coin_reward', 'score')
    search_fields = ('name',)

admin.site.register(Achievement, AchievementAdmin)

# Register the admin class for the Account model
admin.site.register(Account, AccountAdmin)
