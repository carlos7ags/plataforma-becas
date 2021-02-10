from django.conf import settings
from django.db import models


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

    id = models.AutoField(primary_key=True)
    folio = models.CharField("Folio", max_length=16, unique=True)
    convocatoria = models.ForeignKey(
        to=Convocatorias,
        on_delete=models.CASCADE,
        verbose_name="Convocatoria",
    )
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Estudiante",
    )
    grade = models.FloatField("Calificación", null=True)
    socioeconomic_score = models.FloatField("Estudio socioeconómico", null=True)
    comments = models.TextField(
        "Comentarios",
        null=True,
        blank=True,
        help_text="Este campo es obligatorio para estudiantes prioritarios.",
    )
    beneficiado = models.BooleanField("Beneficiado", null=True)
    validated = models.BooleanField(default=False)
    prioritario = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    valor_beca = models.FloatField("Valor de la beca", null=True)


    class Meta:
        unique_together = (
            (
                "convocatoria",
                "username",
            ),
        )

    def __str__(self):
        return "%s" % self.folio
