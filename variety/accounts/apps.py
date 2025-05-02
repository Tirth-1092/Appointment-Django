# accounts/apps.py

from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'  # This should match the folder name of your app

    def ready(self):
        # Import the signals module so that your signal handlers are registered.
        import accounts.signals
