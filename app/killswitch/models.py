# Python imports
from typing_extensions import Self

from requests import delete

# Django imports
from django.db import models

from app.killswitch.killswitch import Compatibility


class KillswithcSettings(models.Model):
    """
        Configuration for the kill switch. Set up messages to show up in the app
        when a compatibility issue is raised. 

        This is a singleton model, so there's only one configuration instance
    """

    non_compatible_msg = models.TextField(
        verbose_name="Non compatible message", 
        null=False, 
        default="La versión actual de su aplicación es muy antigua. Por favor, actualiza a una versión nueva desde la tienda.",
        max_length=1000
        )
    upgradable_compatible_msg = models.TextField(
        verbose_name="Upgradable but compatible message", 
        null=False, 
        default="¡Hay una actualización disponible! Descarga la actualización cuanto antes para que puedas disfrutar de las nuevas funciones y mejoras que tenemos para tí",
        max_length=1000
        )
    last_version_msg = models.CharField(
        verbose_name="Last version message", 
        null=False, 
        default="Su aplicación está actualizada",
        max_length=1000
        )

    # Override save method to make this a singleton
    def save(self, *args, **kwargs) -> None:
        self.pk = 1
        return super().save(*args, **kwargs)

    # Do nothing, the only instance should be never deleted    
    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls) -> Self:
        """
            Get the settings object
        """
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj