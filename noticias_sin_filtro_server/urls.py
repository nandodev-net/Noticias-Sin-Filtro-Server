"""noticias_sin_filtro_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Django imports 
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

# Local imports
from app.scraper import urls as scraper_urls
from app.scraper.serializers import HeadlineViewSet

# Third party imports
from rest_framework import routers, serializers, viewsets


router = routers.DefaultRouter()
router.register(r'headlines', HeadlineViewSet)

urlpatterns = [
    path("admin/", admin.site.urls), path("", include(scraper_urls)),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    ]
