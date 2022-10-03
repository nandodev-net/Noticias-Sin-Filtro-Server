# Django imports
from django.views.generic import ListView
from django.urls import reverse_lazy
from datetime import datetime, timedelta

# Local imports
from app.audio_player.models import Audio
from .forms import AudioModelForm

# Third party imports
from django_datatables_view.base_datatable_view import BaseDatatableView
from bootstrap_modal_forms.generic import (
        BSModalCreateView,
        BSModalUpdateView,
        BSModalReadView,
        BSModalDeleteView,
)


class AudioListView(ListView):
    template_name = "index.html"
    queryset = Audio.objects.all()

    def get_context_data(self, **kwargs):

        get, prefill = self.request.GET or {}, {}
        fields = [
            'title',
            'start_date',
            'end_date',
        ]

        for field in fields:
            getter = get.get(field)
            prefillAux = getter if getter else ""
            if field == 'start_date' and not prefill:
                prefillAux = (datetime.now() - timedelta(days=30)
                              ).strftime('%Y-%m-%d')
            elif field:
                prefill[field] = prefillAux

        context = super().get_context_data()
        context['prefill'] = prefill

        return context



class AudioData(BaseDatatableView):
    "Populate the audios datatable and manage its filters"

    columns = [
        'date',
        'title',
        'audioUrl',
        'listen_count',
        'votes',
    ]

    order_columns = [
        'date',
        'title',
        'audioUrl',
        'listen_count',
        'votes',
    ]

    def get_initial_queryset(self):
        return Audio.objects.all()

    def filter_queryset(self, qs):

        # Get request params
        get = self.request.GET or {}

        title, start_date, end_date = get.get(
            'title'), get.get('start_date'), get.get('end_date')

        if title is not None and title != "":
            qs = qs.filter(title__contains=title)

        if start_date is not None and start_date != "":
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            qs = qs.filter(start_date__gte=start_date)

        if end_date is not None and end_date != "":
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            qs = qs.filter(end_date__lte=end_date)

        return qs

    def prepare_results(self, qs):

        response = []
        for audio in qs:

            response.append({
                'id': audio.id,
                'title': audio.title,
                'audioUrl': audio.audioUrl,
                'date': audio.created,
                'listen_count': audio.listen_count,
                'votes': audio.votes
            })

        return response


class AudioCreateView(BSModalCreateView):
    template_name = 'audios/create.html'
    form_class = AudioModelForm
    success_message = 'Success: An audio file was created.'
    success_url = reverse_lazy('dashboard:index')


class AudioUpdateView(BSModalUpdateView):
    model = Audio
    template_name = 'audios/update.html'
    form_class = AudioModelForm
    success_message = 'Success: An audio file was updated.'
    success_url = reverse_lazy('dashboard:index')


class AudioReadView(BSModalReadView):
    model = Audio
    template_name = 'audios/read.html'


class AudioDeleteView(BSModalDeleteView):
    model = Audio
    template_name = 'audios/delete.html'
    success_message = 'Success: An audio file was deleted.'
    success_url = reverse_lazy('dashboard:index')
