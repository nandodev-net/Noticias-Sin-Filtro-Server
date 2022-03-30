"""
    Router for v0.0.1 api, main changes are:
        + Added fields to category and media site
        + Headline model now has a fk to media site instead of just an enum string
"""

# Local imports
from app.scraper.api.v0_0_2.viewsets import (
    CategoryViewSet,
    HeadlineViewSet,
    MediaSiteViewSet,
)

# Third party imports
from rest_framework import routers

# Define router object
router = routers.DefaultRouter()
router.register(r"headlines", HeadlineViewSet, basename="headlines")
router.register(r"categories", CategoryViewSet)
router.register(r"media_sites", MediaSiteViewSet, basename="media_sites")

urls = router.urls