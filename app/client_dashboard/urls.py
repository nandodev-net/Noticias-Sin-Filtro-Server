# Django imports
from django.urls import path

# Local imports
from app.client_dashboard.views import ClientDashboardView

urlpatterns = [
    path("", ClientDashboardView.as_view(), name="home")
]