import datetime as dt
from urllib.request import urlretrieve

from django.db import models
from model_utils.models import TimeStampedModel
from mutagen.mp3 import MP3

from .author import Author


def getDuration(audio_url):
    filename, headers = urlretrieve(audio_url)
    audio = MP3(filename)
    audio_info = audio.info
    print(audio_info)
    return dt.timedelta(seconds=int(audio_info.length))


# Create your models here.
class Audio(TimeStampedModel):
    title = models.CharField(max_length=100)
    listen_count = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    duration = models.DurationField(default=dt.timedelta(seconds=0))
    author = models.ForeignKey(Author, related_name="audios", on_delete=models.CASCADE)
    audioUrl = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.duration = getDuration(self.audioUrl)
        super(Audio, self).save(*args, **kwargs)

    def __str__(self):
        return "({})- {} - {}".format(
            self.id,
            self.title,
            self.author.name,
        )

    def get_thumbnailUrl(self):
        return self.author.thumbnailUrl

    def get_author_name(self):
        return self.author.name
