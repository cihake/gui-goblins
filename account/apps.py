# AppConfig subclass for the 'account' app.
from django.apps import AppConfig

 # Specifies the default primary key field for models in the app.
class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # Specifies the name of the app.
    name = 'account'
