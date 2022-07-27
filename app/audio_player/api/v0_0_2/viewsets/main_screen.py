from rest_framework.response import Response
from rest_framework import generics
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    )
from ..serializers import MainScreenSerializer
from app.audio_player.models import Author
from .utils import build_audio_obj


class MainScreenApiView(generics.GenericAPIView):
    queryset = Author.objects.exclude(audios__isnull=True)
    http_method_names = [u'get']
    serializer_class = MainScreenSerializer


    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if len(queryset)>0:
            # Calculate favorite last capsule

            last_added = []
            most_listened = []
            most_voted = []

            for author in queryset:
                audios = author.audios.all()
                # For each author return the very last added
                try:
                    la_audio = audios.order_by('-created')[0] #TODO quizas cambie a date y alguna logica de favoritos
                    last_added.append(build_audio_obj(la_audio))
                except Exception as e:
                    print(e)
                    pass

                # For each author return the most listened
                try:
                    ml_audio = audios.filter(author__type=Author.AUTH_PODCASTS).order_by('-listen_count')[0]
                    most_listened.append(build_audio_obj(ml_audio))
                except Exception:
                    pass
            
                # For each author return the most voted
                try:
                    mv_audio = audios.filter(author__type=Author.AUTH_PODCASTS).order_by('-votes')[0]
                    most_voted.append(build_audio_obj(mv_audio))
                except Exception:
                    pass
            
            # Serialize data
            main_screen_dic = {
                'last_capsule': [last_added[0]], #TODO cambiar esto
                'recently_added': last_added,
                'news_authors':queryset.filter(type=Author.AUTH_NEWS),
                'podcast_authors': queryset.filter(type=Author.AUTH_PODCASTS),
                'most_voted': most_voted,
                'most_listened': most_listened,
            }

            main_screen_json = MainScreenSerializer(main_screen_dic)

            return Response(main_screen_json.data, status=HTTP_200_OK)
        else:
            return Response(status=HTTP_204_NO_CONTENT)