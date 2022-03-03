"""
    Exposed http endpoints for this app
"""

from django.conf.urls import url
from app.scraper import views

urlpatterns = [
    url(r'^api/crawl/', views.ScrapingManagerView.as_view(), name='crawl'),
]
