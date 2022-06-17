from rest_framework import serializers
from .author import AuthorSerializer


class AudioSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    duration = serializers.DurationField(read_only=True)
    author = serializers.CharField(read_only=True)
    thumbnailUrl = serializers.CharField(read_only=True)
    audioUrl = serializers.CharField(read_only=True)
    listenCount = serializers.IntegerField(read_only=True)
    votes = serializers.IntegerField(read_only=True)


class MainScreenSerializer(serializers.Serializer):
    last_capsule = AudioSerializer(read_only=True, many=True)
    recently_added = AudioSerializer(read_only=True, many=True)
    authors = AuthorSerializer(read_only=True, many=True)
    most_voted = AudioSerializer(read_only=True, many=True)
    most_listened = AudioSerializer(read_only=True, many=True)


class AuthorScreenSerializer(serializers.Serializer):
    audios = AudioSerializer(read_only=True, many=True)
