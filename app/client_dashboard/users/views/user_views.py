# Django imports
from django.views.generic import ListView
from django.urls import reverse_lazy
from datetime import datetime, timedelta

# Local imports
from app.client_dashboard.users.models import CustomUser
from ..forms import UserModelForm


# Third party imports
from django_datatables_view.base_datatable_view import BaseDatatableView
from bootstrap_modal_forms.generic import (
        BSModalCreateView,
        BSModalUpdateView,
        BSModalReadView,
        BSModalDeleteView,
)


class UserListView(ListView):
    template_name = "users/list.html"
    queryset = CustomUser.objects.all()

    def get_context_data(self, **kwargs):

        get, prefill = self.request.GET or {}, {}
        fields = [
            'full_name',
            'email',
        ]

        for field in fields:
            getter = get.get(field)
            prefillAux = getter if getter else ""
            if field:
                prefill[field] = prefillAux

        context = super().get_context_data()
        context['prefill'] = prefill

        return context



class UsersData(BaseDatatableView):
    "Populate the users datatable and manage its filters"

    columns = [
        'news_media',
        'full_name',
        'email',
        'is_admin',
    ]

    order_columns = [
        'news_media',
        'full_name',
        'email',
        'is_admin',
    ]

    def get_initial_queryset(self):
        return CustomUser.objects.all()

    def filter_queryset(self, qs):

        # Get request params
        get = self.request.GET or {}

        full_name, news_media, email = get.get(
            'full_name'), get.get('news_media'), get.get('email')

        if full_name is not None and full_name != "":
            qs = qs.filter(title__contains=full_name)

        if news_media is not None and news_media != "":
            qs = qs.filter(news_media__name__contains=news_media)

        if email is not None and email != "":
            qs = qs.filter(email__contains=email)


        return qs

    def prepare_results(self, qs):

        response = []
        for user in qs:
            if user.news_media:
                media = user.news_media.name
            else:
                media = "not assigned"

            response.append({
                'id': user.id,
                'full_name': user.full_name,
                'email': user.email,
                'is_admin': user.is_admin,
                'news_media': media,
            })

        return response


class UserCreateView(BSModalCreateView):
    template_name = 'users/create.html'
    form_class = UserModelForm
    success_message = 'Success: An audio file was created.'
    success_url = reverse_lazy('dashboard:users_data')


# class AudioUpdateView(BSModalUpdateView):
#     model = CustomUser
#     template_name = 'users/update.html'
#     form_class = AudioModelForm
#     success_message = 'Success: An audio file was updated.'
#     success_url = reverse_lazy('dashboard:index')


class UserReadView(BSModalReadView):
    model = CustomUser
    context_object_name = 'cuser'
    template_name = 'users/read.html'


class UserDeleteView(BSModalDeleteView):
    model = CustomUser
    context_object_name = 'cuser'
    template_name = 'users/delete.html'
    success_message = 'Success: An user was deleted.'
    success_url = reverse_lazy('dashboard:list_users')