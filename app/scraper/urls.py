"""
    Exposed http endpoints for this app
"""

from django.urls import path
from app.scraper import views

urlpatterns = [
    path("api/crawl/", views.ScrapingManagerView.as_view(), name="crawl"),
]
