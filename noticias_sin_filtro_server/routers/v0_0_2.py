"""
    Router for v0.0.1 api, main changes are:
        + Added fields to category and media site
        + Headline model now has a fk to media site instead of just an enum string
"""
# Django imports
from django.urls import path

# Local imports
from app.scraper.api.v0_0_2.viewsets import (
    CategoryViewSet,
    HeadlineViewSet,
    MediaSiteViewSet,
)
from app.feed.api.v0_0_2.viewsets import FeedView
from app.audio_player.api.v0_0_2.viewsets import (
    MainScreenApiView,
    AuthorScreenApiView,
    SearchResultsScreenApiView,
    AuthorSuggestionsApiView
    )

# Third party imports
from rest_framework import routers

# Define router object
router = routers.DefaultRouter()

# Document router
router.get_api_root_view().cls.__name__ = "Api Noticias sin filtro v0.0.2"
router.get_api_root_view().cls.__doc__ = "Version `v0.0.2` of the Noticias Sin Filtro API, **browse more endpoints using the urls provided below.**"

router.register(r"headlines", HeadlineViewSet, basename="headlines")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"media_sites", MediaSiteViewSet, basename="media_sites")

urls = [
    path('feed/', FeedView.as_view(), name="feed"),
    path('audio/main/', MainScreenApiView.as_view(), name='audio_main_screen'),
    path('audio/author/<int:pk>/', AuthorScreenApiView.as_view(), name='author_screen'),
    path('audio/search/<str:pk>/', SearchResultsScreenApiView.as_view(), name='search_results_screen'),
    path('audio/suggestions/', AuthorSuggestionsApiView.as_view(), name='search_suggestions_screen'),
]

urls += router.urls