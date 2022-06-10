from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.
class Author(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank= True, null= True)
    thumbnailUrl = models.CharField(max_length=200, blank= True, null= True)

    def __str__(self):
        return '({})- {}'.format(
            self.id,
            self.name,
        )