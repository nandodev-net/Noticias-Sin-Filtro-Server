from django.urls import path

from app.audio_player.api.v0_0_2.viewsets import (AudioVoteApiView,
                                                  AuthorFollowApiView,
                                                  AuthorScreenApiView,
                                                  AuthorSuggestionsApiView,
                                                  MainScreenApiView,
                                                  SearchResultsScreenApiView)

app_name = "audio_player"

urlpatterns = [
    path("main/", MainScreenApiView.as_view(), name="audio_main"),
    path("author/<int:pk>/", AuthorScreenApiView.as_view(), name="audio_author"),
    path("search/<str:pk>/", SearchResultsScreenApiView.as_view(), name="audio_search"),
    path("suggestions/", AuthorSuggestionsApiView.as_view(), name="audio_suggestions"),
    path(
        "author/follow/<int:pk>/<int:opt>/",
        AuthorFollowApiView.as_view(),
        name="author_follow",
    ),
    path(
        "audio/vote/<int:pk>/<int:opt>/", AudioVoteApiView.as_view(), name="audio_vote"
    ),
]
