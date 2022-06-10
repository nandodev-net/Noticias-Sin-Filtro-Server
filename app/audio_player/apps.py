from tabnanny import verbose
from django.apps import AppConfig


class AudioPlayerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.audio_player'
    verbose_name = "AudioPlayer"
