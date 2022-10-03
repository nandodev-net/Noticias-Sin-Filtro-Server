from django.urls import path
from . import views

app_name = 'audios'

urlpatterns = [

    path(
        '',
        views.AudioData.as_view(),
        name="list_audios"
    ),
    path(
        'data/',
        views.AudioListView.as_view(),
        name="audios_data"
    ),
    path(
        'create/',
        views.AudioCreateView.as_view(),
        name="audio_create"
    ),
    path(
        'update/<int:pk>',
        views.AudioUpdateView.as_view(),
        name="audio_update"
    ),
    path(
        'read/<int:pk>',
        views.AudioReadView.as_view(),
        name="audio_read"
    ),
    path(
        'delete/<int:pk>',
        views.AudioDeleteView.as_view(),
        name="audio_delete"
    ),
]
