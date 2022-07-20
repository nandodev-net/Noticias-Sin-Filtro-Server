from django.urls import path

from app.audio_player.api.v0_0_2.viewsets import (
    MainScreenApiView,
    AuthorScreenApiView,
    SearchResultsScreenApiView,
    AuthorSuggestionsApiView
    )

app_name = 'audio_player'

urlpatterns = [
    path('main/', MainScreenApiView.as_view(), name='audio_main'),
    path('author/<int:pk>/', AuthorScreenApiView.as_view(), name='audio_author'),
    path('search/<str:pk>/', SearchResultsScreenApiView.as_view(), name='audio_search'),
    path('suggestions/', AuthorSuggestionsApiView.as_view(), name='audio_suggestions'),

]