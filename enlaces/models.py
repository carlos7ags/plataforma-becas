from django.conf import settings
from django.db import models

from becas.models import Universities


class Enlaces(models.Model):
    """Información personal"""

    enlace_id = models.AutoField(primary_key=True)
    username = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    nombre = models.CharField("Nombre(s)", max_length=25)
    primer_apellido = models.CharField("Apellido paterno", max_length=15)
    segundo_apellido = models.CharField("Apellido materno", max_length=15)
    university = models.ForeignKey(
        to=Universities,
        on_delete=models.CASCADE,
        verbose_name="Universidad",
    )

    def __str__(self):
        return "%s - %s" % (self.username, self.university)
