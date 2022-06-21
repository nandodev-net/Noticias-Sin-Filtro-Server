from django.db.models import Q
from rest_framework.response import Response
from django.http import Http404
from rest_framework import generics
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    )
from ..serializers import AudioSerializer, AuthorSuggestionsSerializer
from app.audio_player.models import Audio, Author
from .utils import build_audio_obj

from app.core.pagination import VIPagination


class SearchResultsScreenApiView(generics.GenericAPIView):
    http_method_names = [u'get']
    serializer_class = AudioSerializer
    queryset = Audio.objects.all()

    def get_object(self, pk):
        try:
            return Audio.objects.filter(Q(title__icontains=pk.lower()) | \
                Q(author__name__icontains=pk.lower()))
        except Audio.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        paginator = VIPagination()
        paginator.page_size = 10

        #author = self.get_queryset(self.kwargs['id'])
        audios_ = self.get_object(pk)
        audios = [build_audio_obj(audio_obj) for audio_obj in audios_]

        if len(audios)>0:
            result_page = paginator.paginate_queryset(audios, request)
            author_screen_json = AudioSerializer(result_page, many=True)
        else:
            author_screen_json = AudioSerializer([], many=True)

        try:
            return paginator.get_paginated_response(author_screen_json.data)
        except:
            return Response(status=HTTP_204_NO_CONTENT)

    
class AuthorSuggestionsApiView(generics.GenericAPIView):
    queryset = Author.objects.exclude(audios__isnull=True)
    http_method_names = [u'get']
    serializer_class = AuthorSuggestionsSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            search_suggestions_json = AuthorSuggestionsSerializer(queryset, many=True)
            return Response(search_suggestions_json.data, status=HTTP_200_OK)
        else:
            return Response(status=HTTP_204_NO_CONTENT)