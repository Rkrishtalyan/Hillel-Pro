# ---- Imports ----
from django.apps import AppConfig


# ---- App Configuration ----

class BoardConfig(AppConfig):
    """
    Configuration for the board app, including signal registration.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'board'

    def ready(self):
        """
        Import signals module to ensure signal handlers are registered.
        """
        import board.signals
