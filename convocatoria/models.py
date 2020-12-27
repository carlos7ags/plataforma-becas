from django.db import models


class Modalidades(models.Model):
    modalidad_id = models.AutoField(primary_key=True)
    modalidad = models.CharField("Modalidad", max_length=30)

    def __str__(self):
        return "%s" % self.modalidad


class Convocatorias(models.Model):
    """Información convocatorias"""

    convocatoria_id = models.AutoField(primary_key=True
    )
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
    #presupuesto = models.IntegerField("Presupuesto asignado")

    def __str__(self):
        return "%s" % self.name