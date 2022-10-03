# Django imports
from django.views.generic import ListView
from django.urls import reverse_lazy
from datetime import datetime, timedelta

# Local imports
from app.audio_player.models import Author
from .forms import AuthorModelForm

# Third party imports
from django_datatables_view.base_datatable_view import BaseDatatableView
from bootstrap_modal_forms.generic import (
        BSModalCreateView,
        BSModalUpdateView,
        BSModalReadView,
        BSModalDeleteView,
)


class AuthorListView(ListView):
    template_name = "authors/list.html"
    queryset = Author.objects.all()

    def get_context_data(self, **kwargs):

        get, prefill = self.request.GET or {}, {}
        fields = [
            'name',
            'type',
        
        ]

        for field in fields:
            getter = get.get(field)
            prefillAux = getter if getter else ""
            prefill[field] = prefillAux

        context = super().get_context_data()
        context['prefill'] = prefill

        return context



class AuthorData(BaseDatatableView):
    "Populate the author datatable and manage its filters"

    columns = [
        'thumbnailUrl',
        'name',
        'type',
    ]

    order_columns = [
        'thumbnailUrl',
        'name',
        'type',
    ]

    def get_initial_queryset(self):
        return Author.objects.all()

    def filter_queryset(self, qs):

        # Get request params
        get = self.request.GET or {}

        name, type = get.get('name'), get.get('type')

        if name is not None and name != "":
            qs = qs.filter(name__contains=name)

        if type is not None and name != "":
            qs = qs.filter(type=type)

        return qs

    def prepare_results(self, qs):

        response = []
        for author in qs:

            response.append({
                'id': author.id,
                'name': author.name,
                'type': author.type,
                'thumbnailUrl': author.thumbnailUrl,
            })

        return response


class AuthorCreateView(BSModalCreateView):
    template_name = 'authors/create.html'
    form_class = AuthorModelForm
    success_message = 'Success: An author file was created.'
    success_url = reverse_lazy('dashboard:index')


class AuthorUpdateView(BSModalUpdateView):
    model = Author
    template_name = 'authors/update.html'
    form_class = AuthorModelForm
    success_message = 'Success: An author file was updated.'
    success_url = reverse_lazy('dashboard:index')


class AuthorReadView(BSModalReadView):
    context_object_name = 'author'
    model = Author
    template_name = 'authors/read.html'


class AuthorDeleteView(BSModalDeleteView):
    context_object_name = 'author'
    model = Author
    template_name = 'authors/delete.html'
    success_message = 'Success: An author file was deleted.'
    success_url = reverse_lazy('dashboard:index')
