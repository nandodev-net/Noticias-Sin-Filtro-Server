from rest_framework.response import Response
from django.http import Http404
from rest_framework import generics
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    )

from app.audio_player.models import Audio


class VotedAudioCounterApiView(generics.GenericAPIView):
    http_method_names = [u'get']
    queryset = Audio.objects.all()

    def get_object(self, pk):
        try:
            return Audio.objects.get(id=pk)
        except Audio.DoesNotExist:
            raise Http404

    #def get(self, request, *args, **kwargs):
    def get(self, request, pk, option):
        audio_obj = self.get_object(pk)
        if option == 1:
            audio_obj.votes = audio_obj.votes + 1
            audio_obj.save()
        elif audio_obj.votes > 0 and option == 0:
            audio_obj.votes = audio_obj.votes - 1
            audio_obj.save()
        else:
            pass
        return Response(status=HTTP_200_OK)


class AudioListenCounterApiView(generics.GenericAPIView):
    http_method_names = [u'get']
    queryset = Audio.objects.all()

    def get_object(self, pk):
        try:
            return Audio.objects.get(id=pk)
        except Audio.DoesNotExist:
            raise Http404

    #def get(self, request, *args, **kwargs):
    def get(self, request, pk):
        audio_obj = self.get_object(pk)
        audio_obj.listen_count = audio_obj.listen_count + 1
        audio_obj.save()
        return Response(status=HTTP_200_OK)


