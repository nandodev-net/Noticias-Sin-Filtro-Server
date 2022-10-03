from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [

    path(
        '',
        views.AuthorData.as_view(),
        name="list_authors"
    ),
    path(
        'data/',
        views.AuthorListView.as_view(),
        name="authors_data"
    ),
    path(
        'create/',
        views.AuthorCreateView.as_view(),
        name="author_create"
    ),
    path(
        'update/<int:pk>',
        views.AuthorUpdateView.as_view(),
        name="author_update"
    ),
    path(
        'read/<int:pk>',
        views.AuthorReadView.as_view(),
        name="author_read"
    ),
    path(
        'delete/<int:pk>',
        views.AuthorDeleteView.as_view(),
        name="author_delete"
    ),
]
