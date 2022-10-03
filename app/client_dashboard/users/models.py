from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext as _

from .managers import CustomUserManager
from app.audio_player.models import Author


class CustomUser(AbstractBaseUser, PermissionsMixin):

    news_media = models.ForeignKey(Author, blank= True, null= True , on_delete=models.CASCADE)

    full_name = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    email = models.EmailField(_('email address'),
                              unique=True
                              )

    is_admin = models.BooleanField(
        default=False
    )

    is_editor = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=True
    )

    is_active = models.BooleanField(
        default=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', ]

    objects = CustomUserManager()

    def __str__(self):
        return self.email