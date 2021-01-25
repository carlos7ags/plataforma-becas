from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
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
    numero_int = models.IntegerField("Número interior", null=True, blank=True)
    colonia = models.CharField("Colonia", max_length=100)
    cp = models.IntegerField(
        "Código postal",
        validators=[MinValueValidator(20000), MaxValueValidator(20999)],
    )
    localidad = models.CharField("Localidad", max_length=100)
    municipio = models.ForeignKey(
        to=Municipios,
        on_delete=models.CASCADE,
        verbose_name="Municipio",
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
    continua = models.BooleanField(
        "En caso de TSU, planeo continuar con mis estudios a nivel licenciatura o ingeniería.",
        max_length=30,
    )
    programa = models.ForeignKey(
        to=Programs,
        on_delete=models.CASCADE,
        verbose_name="Programa",
    )
    nivel_actual = models.IntegerField("Semestre/Cuatrimestre actual")
    promedio = models.FloatField("Promedio general")

    def __str__(self):
        return "%s" % self.username


############################################################################################################
#                                        Estudio Socio Económico                                           #
############################################################################################################


class MaritalStatus(models.Model):
    """Estado civil"""

    marital_status_id = models.AutoField(primary_key=True)
    marital_status = models.CharField(
        "Estado Civil",
        max_length=50,
    )

    def __str__(self):
        return "%s" % self.marital_status


class PovertyRange(models.Model):
    """Rangos de pobreza de acuerdo con CONEVAL"""

    poverty_id = models.AutoField(primary_key=True)
    poverty = models.CharField(
        "Rango de pobreza de su colonia",
        max_length=30,
    )
    value = models.IntegerField("Puntuación")

    def __str__(self):
        return "%s" % self.poverty


class AverageGradeRanges(models.Model):
    """Rangos de promedio general"""

    average_grade_range_id = models.AutoField(primary_key=True)
    average_grade_range = models.CharField(
        "Promedio general",
        max_length=30,
    )
    value = models.IntegerField("Puntuación")

    def __str__(self):
        return "%s" % self.average_grade_range


class FamilyMembersRange(models.Model):
    """Rangos de integrantes de familia"""

    family_members_range_id = models.AutoField(primary_key=True)
    family_members_range = models.CharField(
        "Número de integrantes de la familia",
        max_length=50,
    )
    value = models.IntegerField("Puntuación")

    def __str__(self):
        return "%s" % self.family_members_range


class FamilyMonthlyIncome(models.Model):
    """Ingresos familiares"""

    family_monthly_income_id = models.AutoField(primary_key=True)
    family_monthly_income = models.CharField(
        "Ingreso familiar mensual",
        max_length=50,
    )
    value = models.IntegerField("Puntuación")

    def __str__(self):
        return "%s" % self.family_monthly_income


class ParentsEducationLevel(models.Model):
    """Ingresos familiares"""

    parent_education_level_id = models.AutoField(primary_key=True)
    parent_education_level = models.CharField(
        "Nivel educativo del padre/madre",
        max_length=50,
    )
    value = models.IntegerField("Puntuación")

    def __str__(self):
        return "%s" % self.parent_education_level


class SocialSecurity(models.Model):
    """Seguridad social"""

    social_security_id = models.AutoField(primary_key=True)
    social_security = models.CharField(
        "Afiliación a servicios de salud y seguridad social",
        max_length=50,
    )
    value = models.IntegerField("Puntuación")

    def __str__(self):
        return "%s" % self.social_security


class ProviderPerks(models.Model):
    """Seguridad social"""

    provider_perks_id = models.AutoField(primary_key=True)
    provider_perks = models.CharField(
        "Principal proveedor con prestaciones",
        max_length=50,
    )
    value = models.IntegerField("Puntuación")

    def __str__(self):
        return "%s" % self.provider_perks


class HomeType(models.Model):
    """Seguridad social"""

    home_type_id = models.AutoField(primary_key=True)
    home_type = models.CharField(
        "Tipo de vivienda",
        max_length=50,
    )
    value = models.IntegerField("Puntuación")

    def __str__(self):
        return "%s" % self.home_type


class HomeFloor(models.Model):
    """Seguridad social"""

    home_floor_id = models.AutoField(primary_key=True)
    home_floor = models.CharField(
        "Tipo de piso de la vivienda",
        max_length=50,
    )
    value = models.IntegerField("Puntuación")

    def __str__(self):
        return "%s" % self.home_floor


class HomeCeil(models.Model):
    """Seguridad social"""

    home_ceil_id = models.AutoField(primary_key=True)
    home_ceil = models.CharField(
        "Tipo de techo de la vivienda",
        max_length=50,
    )
    value = models.IntegerField("Puntuación")

    def __str__(self):
        return "%s" % self.home_ceil


class HomeWalls(models.Model):
    """Seguridad social"""

    home_walls_id = models.AutoField(primary_key=True)
    home_walls = models.CharField(
        "Tipo de muros de la vivienda",
        max_length=50,
    )
    value = models.IntegerField("Puntuación")

    def __str__(self):
        return "%s" % self.home_walls


class HomePersons(models.Model):
    """Seguridad social"""

    home_persons_id = models.AutoField(primary_key=True)
    home_persons = models.CharField(
        "Número de personas por habitación",
        max_length=50,
    )
    value = models.IntegerField("Puntuación")

    def __str__(self):
        return "%s" % self.home_persons


class ServiceWater(models.Model):
    """Seguridad social"""

    service_water_id = models.AutoField(primary_key=True)
    service_water = models.CharField(
        "Agua potable",
        max_length=50,
    )
    value = models.IntegerField("Puntuación")

    def __str__(self):
        return "%s" % self.service_water


class ServiceElectricity(models.Model):
    """Seguridad social"""

    service_electricity_id = models.AutoField(primary_key=True)
    service_electricity = models.CharField(
        "Electricidad",
        max_length=50,
    )
    value = models.IntegerField("Puntuación")

    def __str__(self):
        return "%s" % self.service_electricity


class ServiceSewer(models.Model):
    """Seguridad social"""

    service_sewer_id = models.AutoField(primary_key=True)
    service_sewer = models.CharField(
        "Drenaje",
        max_length=50,
    )
    value = models.IntegerField("Puntuación")

    def __str__(self):
        return "%s" % self.service_sewer


class ServiceGas(models.Model):
    """Seguridad social"""

    service_gas_id = models.AutoField(primary_key=True)
    service_gas = models.CharField(
        "Combustible para cocinar",
        max_length=50,
    )
    value = models.IntegerField("Puntuación")

    def __str__(self):
        return "%s" % self.service_gas


class SocioEconomicStudy(models.Model):
    """Formato de estudio socioeconómico"""

    username = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        primary_key=True,
    )
    marital_status = models.ForeignKey(
        to=MaritalStatus,
        on_delete=models.CASCADE,
        verbose_name="Estado civil",
    )
    poverty_range = models.ForeignKey(
        to=PovertyRange,
        on_delete=models.CASCADE,
        verbose_name="Rango de pobreza de su colonia",
        help_text="Puedes consultar la clasificación de tu colonia en el siguiente vínculo: "
                  "https://www.coneval.org.mx/Medicion/IRS/Paginas/Rezago_social_AGEB_2010.aspx\n "
                  "Te recordamos que proporcionar información falsa o imprecisa descalificará tu solicitud.",
    )
    average_grade_range = models.ForeignKey(
        to=AverageGradeRanges,
        on_delete=models.CASCADE,
        verbose_name="Promedio general",
    )
    family_members = models.ForeignKey(
        to=FamilyMembersRange,
        on_delete=models.CASCADE,
        verbose_name="Número de integrantes de la familia",
    )
    # ToDo: Replace with dynamic forms
    dad_occupation = models.CharField(
        "Ocupación del padre ", max_length=30, null=True, blank=True
    )
    dad_income = models.FloatField(
        "Ingresos mensuales del padre ", blank=True, null=True
    )
    mom_occupation = models.CharField(
        "Ocupación de la madre ", max_length=30, null=True, blank=True
    )
    mom_income = models.FloatField(
        "Ingresos mensuales de la madre ", blank=True, null=True
    )
    son_occupation = models.CharField(
        "Ocupación del hijo ", max_length=30, null=True, blank=True
    )
    son_income = models.FloatField(
        "Ingresos mensuales del hijo ", blank=True, null=True
    )
    candidate_occupation = models.CharField(
        "Ocupación del candidato ", max_length=30, null=True, blank=True
    )
    candidate_income = models.FloatField(
        "Ingresos mensuales del candidato ", blank=True, null=True
    )
    other_occupation = models.CharField(
        "Ocupación del candidato ", max_length=30, null=True, blank=True
    )
    other_income = models.FloatField(
        "Ingresos mensuales del candidato ", blank=True, null=True
    )
    family_monthly_income = models.ForeignKey(
        to=FamilyMonthlyIncome,
        on_delete=models.CASCADE,
        verbose_name="Ingreso familiar mensual",
    )
    exp_food = models.FloatField(
        "Gastos mensuales aproximados en comida ", blank=True, null=True
    )
    exp_rent = models.FloatField(
        "Gastos mensuales aproximados en renta/hipoteca ", blank=True, null=True
    )
    exp_water = models.FloatField(
        "Gastos mensuales aproximados en  el  servicio de agua", blank=True, null=True
    )
    exp_energy = models.FloatField(
        "Gastos mensuales aproximados en el servicio de electricidad",
        blank=True,
        null=True,
    )
    exp_leisure = models.FloatField(
        "Gastos mensuales aproximados dedicados a la diversión ",
        blank=True,
        null=True,
    )
    exp_transport = models.FloatField(
        "Gastos mensuales aproximados dedicados al transporte", blank=False, null=False
    )
    exp_education = models.FloatField(
        "Gastos mensuales aproximados dedicados a la educación", blank=False, null=False
    )
    exp_telecom = models.FloatField(
        "Gastos mensuales aproximados dedicados a servicios de telefonía, cable e internet",
        blank=True,
        null=True,
    )
    exp_medic = models.FloatField(
        "Gastos mensuales aproximados dedicados a gastos médicos",
        blank=True,
        null=True,
    )
    exp_gas = models.FloatField(
        "Gastos mensuales aproximados dedicados a gas y energía",
        blank=True,
        null=True,
    )
    exp_vestido = models.FloatField(
        "Gastos mensuales aproximados dedicados a vestido",
        blank=True,
        null=True,
    )
    exp_loans = models.FloatField(
        "Gastos mensuales aproximados dedicados a créditos e intereses",
        blank=True,
        null=True,
    )
    exp_gasolina = models.FloatField(
        "Gastos mensuales aproximados dedicados a gasolina",
        blank=True,
        null=True,
    )
    exp_otros = models.FloatField("Otros gastos ", blank=True, null=True)

    education_level_father = models.ForeignKey(
        to=ParentsEducationLevel,
        on_delete=models.CASCADE,
        verbose_name="Escolaridad del padre",
        related_name="education_level_father",
    )
    education_level_mother = models.ForeignKey(
        to=ParentsEducationLevel,
        on_delete=models.CASCADE,
        verbose_name="Escolaridad de la madre",
        related_name="education_level_mother",
    )
    education_level_partner = models.ForeignKey(
        to=ParentsEducationLevel,
        on_delete=models.CASCADE,
        verbose_name="Escolaridad de la esposa(o)",
        related_name="education_level_partner",
    )
    social_security = models.ForeignKey(
        to=SocialSecurity,
        on_delete=models.CASCADE,
        verbose_name="Afiliación a servicios de salud y seguridad social",
    )
    provider_perks = models.ForeignKey(
        to=ProviderPerks,
        on_delete=models.CASCADE,
        verbose_name="Principal proveedor en el hogar cuenta con prestaciones",
    )
    home_type = models.ForeignKey(
        to=HomeType,
        on_delete=models.CASCADE,
        verbose_name="Tipo de vivienda",
    )
    home_floor = models.ForeignKey(
        to=HomeFloor,
        on_delete=models.CASCADE,
        verbose_name="Tipo de piso de la vivienda",
    )
    home_ceil = models.ForeignKey(
        to=HomeCeil,
        on_delete=models.CASCADE,
        verbose_name="Tipo de techo de la vivienda",
    )
    home_walls = models.ForeignKey(
        to=HomeWalls,
        on_delete=models.CASCADE,
        verbose_name="Tipo de muros de la vivienda",
    )
    home_persons = models.ForeignKey(
        to=HomePersons,
        on_delete=models.CASCADE,
        verbose_name="Número de personas por habitación",
    )
    service_water = models.ForeignKey(
        to=ServiceWater,
        on_delete=models.CASCADE,
        verbose_name="Agua potable",
    )
    service_electricity = models.ForeignKey(
        to=ServiceElectricity,
        on_delete=models.CASCADE,
        verbose_name="Electricidad",
    )
    service_sewer = models.ForeignKey(
        to=ServiceSewer,
        on_delete=models.CASCADE,
        verbose_name="Drenaje",
    )
    service_gas = models.ForeignKey(
        to=ServiceGas,
        on_delete=models.CASCADE,
        verbose_name="Coombustible para cocinar",
    )

    last_update = models.DateTimeField(auto_now=True)
