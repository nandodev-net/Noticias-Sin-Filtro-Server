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
from noticias_sin_filtro_server.routers.v0_0_1 import urls as urls_v001
from noticias_sin_filtro_server.versioning.viewsets import KillSwitchViewSet

urlpatterns = [
    path("admin/", admin.site.urls), path("", include(scraper_urls)),
    path("version/", view=KillSwitchViewSet.as_view({"get" : "get"})),
    path('v0.0.1/', include(urls_v001)),
    path('api-auth/', include('rest_framework.urls')),
    ]
