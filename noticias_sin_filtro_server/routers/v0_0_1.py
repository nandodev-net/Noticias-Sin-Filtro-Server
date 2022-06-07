"""
    Router for v0.0.1 api 
"""

# Local imports
from app.scraper.api.v0_0_1.viewsets import (
    CategoryViewSet,
    HeadlineViewSet,
    MediaSiteViewSet,
)

# Third party imports
from rest_framework import routers

# Define router object
router = routers.DefaultRouter()

# Document router
router.get_api_root_view().cls.__name__ = "Api Noticias sin filtro v0.0.1"
router.get_api_root_view().cls.__doc__ = "Version `v0.0.1` of the Noticias Sin Filtro API, **browse more endpoints using the urls provided below**"

# Register views
router.register(r"headlines", HeadlineViewSet, basename="headlines")
router.register(r"categories", CategoryViewSet)
router.register(r"media_sites", MediaSiteViewSet, basename="media_sites")

urls = router.urls
