from django.apps import AppConfig


class ClientDashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.client_dashboard'
    verbose_name: str = 'Client Dashboard'
