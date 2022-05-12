from tabnanny import verbose
from django.apps import AppConfig

class KillswitchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.killswitch'
    verbose_name = "Killswitch"
