from rest_framework.response import Response
from django.http import Http404
from rest_framework import generics
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    )
from app.audio_player.models import Author, Audio
from ..serializers import AuthorSerializer, AudioSerializer


class AuthorFollowApiView(generics.GenericAPIView):
    http_method_names = [u'get']
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get_object(self, pk):
        try:
            return Author.objects.get(id=pk)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, pk, opt):

        author = self.get_object(pk)
        if opt == 1:
            author.followers = author.followers + 1
        else:
            if author.followers >= 1:
                author.followers = author.followers - 1
            else:
                pass
        author.save()
        return Response(status=HTTP_200_OK)


class AudioVoteApiView(generics.GenericAPIView):
    http_method_names = [u'get']
    serializer_class = AudioSerializer
    queryset = Audio.objects.all()

    def get_object(self, pk):
        try:
            return Audio.objects.get(id=pk)
        except Audio.DoesNotExist:
            raise Http404

    def get(self, request, pk, opt):

        audio = self.get_object(pk)
        if opt == 1:
            audio.votes = audio.votes + 1
        else:
            if audio.votes >= 1:
                audio.votes = audio.votes - 1
            else:
                pass
        audio.save()
        return Response(status=HTTP_200_OK)