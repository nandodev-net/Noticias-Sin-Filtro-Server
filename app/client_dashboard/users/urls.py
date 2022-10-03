from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path(
        'user/',
        views.UsersData.as_view(),
        name="list_users"
    ),
        path(
        'user/data/',
        views.UserListView.as_view(),
        name="users_data"
    ),
        path(
        'user/create/',
        views.UserCreateView.as_view(),
        name="users_create"
    ),
    path(
        'read/<int:pk>',
        views.UserReadView.as_view(),
        name="user_read"
    ),
    path(
        'delete/<int:pk>',
        views.UserDeleteView.as_view(),
        name="user_delete"
    ),
]
