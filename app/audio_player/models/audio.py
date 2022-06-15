from django.db import models
import datetime as dt
from model_utils.models import TimeStampedModel
from .author import Author


# Create your models here.
class Audio(TimeStampedModel):
    title = models.CharField(max_length=100)
    listen_count = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    duration = models.DurationField(default= dt.timedelta(seconds=0))
    author = models.ForeignKey(Author, related_name='audios' , on_delete=models.CASCADE)
    audioUrl = models.CharField(max_length=200, blank= True, null= True)
    date = models.DateTimeField(null = True, blank = True)

    def __str__(self):
        return '({})- {} - {}'.format(
            self.id,
            self.title,
            self.author.name,
        )
    
    def get_thumbnailUrl(self):
        return self.author.thumbnailUrl

    def get_author_name(self):
        return self.author.name