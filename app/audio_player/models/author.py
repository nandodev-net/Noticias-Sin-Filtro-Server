from django.db import models
from model_utils.models import TimeStampedModel


# Create your models here.
class Author(TimeStampedModel):
    AUTH_NEWS = "News"
    AUTH_PODCASTS = "Podcast"
    TYPE_MAXLENGTH = 25

    AUTH_TYPE = ((AUTH_NEWS, AUTH_NEWS), (AUTH_PODCASTS, AUTH_PODCASTS))
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True, null=True)
    thumbnailUrl = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(
        choices=AUTH_TYPE, max_length=TYPE_MAXLENGTH, default=AUTH_NEWS
    )
    followers = models.IntegerField(default=0)

    def __str__(self):
        return "({})- {}".format(
            self.id,
            self.name,
        )
