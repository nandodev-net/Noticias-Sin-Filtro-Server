# Django imports
from django.urls import path, include
from django.contrib.auth import views as auth
from .users import views as user_view
from app.client_dashboard.users import urls as users_urls
# Local imports
from app.client_dashboard.views import ClientDashboardView

urlpatterns = [
    path("", include(users_urls)),
    path('login/', user_view.Login, name ='login'),
    path('logout/', auth.LogoutView.as_view(template_name ='index.html'), name ='logout'),
    path('register/', user_view.register, name ='register'),
]