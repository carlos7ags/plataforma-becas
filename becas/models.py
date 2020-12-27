from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.conf import settings


class Estados(models.Model):
    estado_id = models.AutoField(primary_key=True)
    estado = models.CharField("Estado", max_length=30)

    def __str__(self):
        return "%s" % self.estado


class Municipios(models.Model):
    municipio_id = models.AutoField(primary_key=True)
    municipio = models.CharField("Municipio", max_length=30)

    def __str__(self):
        return "%s" % self.municipio


class Student(models.Model):
    """Información personal"""

    username = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        primary_key=True,
    )
    student_id = models.CharField("ID Estudiante", max_length=30)
    nombre = models.CharField("Nombre(s)", max_length=30)
    primer_apellido = models.CharField("Apellido paterno", max_length=15)
    segundo_apellido = models.CharField("Apellido materno", max_length=15)
    fecha_nacimiento = models.DateField("Fecha de nacimiento")
    lugar_nacimiento = models.ForeignKey(
        to=Estados,
        on_delete=models.CASCADE,
        verbose_name="Lugar de nacimiento",
    )
    ine = models.CharField(
        "INE",
        max_length=13,
        null=True,
        blank=True,
        help_text='Registra los 13 digitos que siguen a los simbolos "<<" en la parte posterior de tu INE.',
        validators=[
            RegexValidator(
                regex=r"([0-9]{13})",
                message="Ingresa una clave INE válida.",
                code="invalid_ine",
            )
        ],
    )

    """Datos de contacto"""
    calle = models.CharField("Calle", max_length=100)
    numero_ext = models.IntegerField("Número exterior")
    numero_int = models.IntegerField(
        "Número interior", null=True, blank=True
    )
    colonia = models.CharField("Colonia", max_length=100)
    cp = models.IntegerField(
        "Código postal",
        validators=[MinValueValidator(20000), MaxValueValidator(20999)],
    )
    localidad = models.CharField("Localidad", max_length=100)
    municipio = models.ForeignKey(
        to=Municipios, on_delete=models.CASCADE, verbose_name="Municipio",
    )
    telefono = models.CharField(
        "Teléfono fijo",
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"([0-9]{10})",
                message="Ingresa un teléfono válido de 10 dígitos.",
                code="invalid_phone",
            )
        ],
    )
    celular = models.CharField(
        "Celular",
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"([0-9]{10})",
                message="Ingresa un teléfono válido de 10 digitos.",
                code="invalid_phone",
            )
        ],
    )

    def __str__(self):
        return "%s" % self.username


class Universities(models.Model):

    university_id = models.AutoField(primary_key=True)
    university = models.CharField("Universidad", max_length=30)

    def __str__(self):
        return "%s" % self.university


class Modalidades(models.Model):

    modalidad_id = models.AutoField(primary_key=True)
    modalidad = models.CharField("Modalidad", max_length=30)

    def __str__(self):
        return "%s" % self.modalidad


class Grados(models.Model):
    grado_id = models.AutoField(primary_key=True)
    grado = models.CharField("Modalidad", max_length=30)

    def __str__(self):
        return "%s" % self.grado


class Programs(models.Model):
    program_id = models.AutoField(primary_key=True)
    programa = models.CharField("Programa", max_length=128)
    university = models.ForeignKey(
        to=Universities,
        on_delete=models.CASCADE,
        verbose_name="Universidad",
    )
    grado = models.ForeignKey(
        to=Grados,
        on_delete=models.CASCADE,
        verbose_name="Grado",
    )
    modalidad = models.ForeignKey(
        to=Modalidades,
        on_delete=models.CASCADE,
        verbose_name="Modalidad",
    )
    duracion = models.IntegerField("Duración (semestres/cuatrimestres)")


    def __str__(self):
        return "%s" % self.programa


class StudentAcademicProgram(models.Model):
    username = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        primary_key=True,
    )
    university = models.ForeignKey(
        to=Universities,
        on_delete=models.CASCADE,
        verbose_name="Universidad",
    )
    grado = models.ForeignKey(
        to=Grados,
        on_delete=models.CASCADE,
        verbose_name="Grado",
    )
    continua = models.BooleanField("En caso de TSU, planeo continuar con mis estudios a nivel licenciatura o ingeniería.", max_length=30)
    programa = models.ForeignKey(
        to=Programs,
        on_delete=models.CASCADE,
        verbose_name="Programa",
    )
    nivel_actual = models.IntegerField("Semestre/Cuatrimestre actual")
    promedio = models.IntegerField("Promedio general")

    def __str__(self):
        return "%s" % self.username
