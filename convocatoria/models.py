from django.db import models
from django.conf import settings


class Modalidades(models.Model):
    modalidad_id = models.AutoField(primary_key=True)
    modalidad = models.CharField("Modalidad", max_length=30)

    def __str__(self):
        return "%s" % self.modalidad


class Convocatorias(models.Model):
    """Información convocatorias"""

    convocatoria_id = models.AutoField(primary_key=True)
    codigo = models.CharField("Código", max_length=8)
    name = models.CharField("Nombre", max_length=30)
    description = models.CharField("Descripción", max_length=256)
    start_date = models.DateField("Fecha de apertura")
    end_date = models.DateField("Fecha de cierre")
    results_date = models.DateField("Publicación de resultados")
    modalidad = models.ForeignKey(
        to=Modalidades,
        on_delete=models.CASCADE,
        verbose_name="Modalidad",
    )
    presupuesto = models.IntegerField("Presupuesto asignado")

    def __str__(self):
        return "%s" % self.name


class Aspirantes(models.Model):
    """Información convocatorias"""

    folio = models.AutoField(primary_key=True)
    convocatoria = models.ForeignKey(
        to=Convocatorias,
        on_delete=models.CASCADE,
        verbose_name="Convocatoria",
    )
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
    )
    grade = models.IntegerField("Calificación", null=True)
    socioeconomic_score = models.IntegerField("Estudio socioeconómico", null=True)
    general_score = models.IntegerField("Score", null=True)
    beneficiado = models.BooleanField("Beneficiado", null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.folio
