
# Django imports
from django.shortcuts import render
from django.views.generic import TemplateView


class ClientDashboardView(TemplateView):
    """
        Main view used by our clients to manage their 
        audio files
    """

    template_name: str = "index.html"
