from rest_framework import serializers
from app.audio_player.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class AuthorSuggestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']
