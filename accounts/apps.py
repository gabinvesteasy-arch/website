from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # ⚠️ REMOVE OR COMMENT OUT THIS LINE:
        # import accounts.signals
        pass