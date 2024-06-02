from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from app.audio_player.models import Author
from app.core.pagination import VIPagination

from ..serializers import AudioSerializer
from .utils import build_audio_obj


class AuthorScreenApiView(generics.GenericAPIView):
    http_method_names = ["get"]
    serializer_class = AudioSerializer
    queryset = Author.objects.all()

    def get_object(self, pk):
        try:
            return Author.objects.get(id=pk)
        except Author.DoesNotExist:
            raise Http404

    # def get(self, request, *args, **kwargs):
    def get(self, request, pk):
        paginator = VIPagination()
        paginator.page_size = 10

        # author = self.get_queryset(self.kwargs['id'])
        author = self.get_object(pk)
        audios = [build_audio_obj(audio_obj) for audio_obj in author.audios.all()]

        if len(audios) > 0:
            result_page = paginator.paginate_queryset(audios, request)
            author_screen_json = AudioSerializer(result_page, many=True)
        else:
            author_screen_json = AudioSerializer([], many=True)

        # return Response(author_screen_json.data, status=HTTP_200_OK)
        try:
            return paginator.get_paginated_response(author_screen_json.data)
        except:
            return Response(status=HTTP_204_NO_CONTENT)
