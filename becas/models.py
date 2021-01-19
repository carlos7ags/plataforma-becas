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



############################################################################################################
#                                        Estudio Socio Económico                                           #
############################################################################################################
rp = (('0', 'Muy bajo'), ('1', 'Bajo'), ('2', 'Medio'), ('3', 'Alto'), ('4', 'Muy alto'))

pg = (('0', 'De 8.5 a 9.0'), ('1', 'De 9.1 a 10'))

int_fa = (('0', 'De 1 a 3'), ('1', 'De 4 a 7'), ('2', 'Más de 7'))

ing_fa = (('0', 'De $0 a $3,696 pesos'), ('1', 'Más de $3,696 y hasta $7,393 pesos'), ('2', 'Más de $7,393 y hasta $11,089 pesos'), ('3', 'Más de $11,089 y hasta $14,786 pesos'), ('4', 'Más de $14,786 y hasta $18,483 pesos'), ('4', 'Más de $18,483 pesos'))

ep = (('0', 'Ninguna'), ('1', 'Primaria'), ('2', 'Secundaria'), ('3', 'Preparatoria/Carrera técnica'), ('4', 'Licenciatura'), ('5', 'Maestría/Doctorado'))

em = (('0', 'Ninguna'), ('1', 'Primaria'), ('2', 'Secundaria'), ('3', 'Preparatoria/Carrera técnica'), ('4', 'Licenciatura'), ('5', 'Maestría/Doctorado'))

afi = (('0', 'Ninguno'), ('1', 'Médico particular'), ('2', 'IMSS-ISSSTE-PEMEX-INSABI-Gastos médicos'))

pres = (('0', 'Ninguna prestación'), ('1', 'Servicio médico, sistema de ahorro para retiro, incapacidad laboral con goce de sueldo'))

vi = (('0', 'Prestada'), ('1', 'Rentada'), ('2', 'La están pagando'), ('3', 'Propia'))

pi = (('0', 'Firme de cemento, tierra'), ('1', 'Con recubrimiento (laminado, vitropiso, mosaico, madera)'))

te = (('0', 'Asbesto, palma, teja'), ('1', 'Lámina metálica arto'), ('2', 'Terrado con viguería'), ('3', 'Madera'), ('4', 'Losa de concreto o viguetas con bovedilla'))

mu = (('0', 'Adobe'), ('1', 'Piedra'), ('2', 'Madera'), ('3', 'Block'), ('4', 'Tabique o ladrillo'))

pe_cu = (('0', 'Número  de personas por cuarto mayor a 2.5'), ('1', 'Número  de personas por cuarto menor a 2.5'))

ag = (('0', 'Si'), ('1', 'No'))

dre = (('0', 'Si'), ('1', 'No'))

ele = (('0', 'Si'), ('1', 'No'))

comb = (('0', 'Si'), ('1', 'No'))

op = ['1 - 0% (De 0 a 10 puntos)', '2 - 25% (De 11 a 20 puntos)', '3 - 50% (De 21 a 31 puntos)', '4 - 75% (De 31 a 41 puntos)', '5 - 100% (41 puntos o más)']
OP = [(str(i),j) for i, j in zip(range(len(op)), op)]

class SocioEconomicStudy(models.Model):
    """Formato de estudio socioeconómico"""
    
    study_id = models.AutoField(primary_key=True)
   
    # I Datos generales del solicitante 
    
    nombre = models.CharField("Nombre(s)", max_length=30)
    primer_apellido = models.CharField("Apellido paterno", max_length=15)
    segundo_apellido = models.CharField("Apellido materno", max_length=15)  

    poverty_range = models.CharField('Rango  de pobreza de su colonia', choices=rp, max_length=100)
    general_average = models.CharField('Promedio General', choices=pg, max_length=100)
    family_integrants= models.CharField('Número de integrantes de la familia', choices=int_fa, max_length=100)
    section1_obs = models.CharField('Observaciones', max_length=100, null=True, blank=False)
    punct_section1 = models.IntegerField('puntuación total obtenida en el apartado ')

    # II Datos Económicos del solicitante 
   
    dad_occupation = models.CharField('Ocupación del padre', max_length=30, null=True, blank=False)
    dad_income = models.FloatField('Ingresos mensuales del padre', blank=False, null=False)
    mom_occupation = models.CharField('Ocupación de la madre', max_length=30, null=True, blank=False)
    mom_income = models.FloatField('Ingresos mensuales de la madre', blank=False, null=False)
    son_occupation = models.CharField('Ocupación del hijo', max_length=30, null=True, blank=False)
    son_income = models.FloatField('Ingresos mensuales del hijo', blank=False, null=False)
    candidate_occupation = models.CharField('Ocupación del candidato', max_length=30, null=True, blank=False)
    candidate_income = models.FloatField('Ingresos mensuales del candidato ', blank=False, null=False)
    candidate_workplace = models.CharField('Lugar de trabajo del candidato', max_length=15, null=True, blank=False)
    family_income = models.CharField('Ingreso total familiar mensual',  choices=ing_fa, max_length=50)
    exp_food = models.FloatField('Gastos mensuales en comida ', blank=False, null=False)
    exp_rent = models.FloatField('Gastos mensuales en renta/hipoteca ', blank=False, null=False)
    exp_water = models.FloatField('Gastos mensuales dedicados al servicio de agua', blank=False, null=False)
    exp_elect = models.FloatField('Gastos mensuales en el servicio de electricidad', blank=False, null=False)
    exp_diversion = models.FloatField('Gastos mensuales dedicados a la diversión ', blank=False, null=False)
    exp_transport = models.FloatField('Gastos mensuales dedicados al transporte', blank=False, null=False)
    exp_education = models.FloatField('Gastos mensuales dedicados a la educación', blank=False, null=False)
    exp_tv_internet = models.FloatField('Gastos mensuales dedicados a servicios de cable Tv e internet', blank=False, null=False)
    exp_otros =models.FloatField('Otros gastos ', blank=False, null=False)
    section2_obs = models.CharField('Observaciones', max_length=100, null=True, blank=False)
    punct_section2 = models.IntegerField('puntuación total obtenida en el apartado ')


    # III Educación 

    dad_scholar = models.CharField('Escolaridad del padre o tutor', choices=ep, max_length=100)
    mom_scholar = models.CharField('Escolaridad de la madre', choices=em, max_length=100)
    cand_scholar = models.CharField('Escolaridad del candidato', choices=ep, max_length=100)
    spous_scholar = models.CharField('Escolaridad del esposo/a', choices=em, max_length=100)
    section3_obs = models.CharField('Observaciones', max_length=100, null=True, blank=False)
    punct_section3 = models.IntegerField('puntuación total obtenida en el apartado ')

    # IV  Salud y seguridad Social 

    healt_prov = models.CharField('El principal proveedor en el hogar está registrado o afiliado en:', choices=afi, max_length=100)
    employment_benefits = models.CharField(
        'Principal proveedor en el hogar económicamente activo, asalariado con todas y cada una de las siguientes prestaciones laborales:',
         choices=pres, max_length=100)
    section4_obs = models.CharField('Observaciones', max_length=100, null=True, blank=False)
    punct_section4 = models.IntegerField('puntuación total obtenida en el apartado ')

    # V Vivienda
   
    home_type = models.CharField('La casa que habita la familia es:', choices=vi, max_length=100)
    floor_type = models.CharField('el piso  de su vivienda es:', choices=pi, max_length=100)
    ceiling_type = models.CharField('El techo de su vivienda es:', choices=vi, max_length=100)
    walls_tipe = models.CharField('Los muros de su vivienda son de:', choices=mu, max_length=100)
    room_persons = models.CharField('Número de personas por cuarto:', choices=pe_cu, max_length=100)
    water_service = models.CharField('¿ Su casa cuenta con servicio de agua entubada dentro de la vivienda o fuera de la vivienda, pero dentro del terreno ?:', choices=ag, max_length=100)
    drain_service = models.CharField('¿ Su casa cuenta con servicio de drenaje conectado a una red pública o a una fora séptica ?:', choices=dre, max_length=100)
    elect_service = models.CharField('¿ Su casa cuenta con servicio de electricidad obtenido del servicio público, de panel solar o de otra fuente, planta paticular?:', choices=ele, max_length=100)
    fuel_service = models.CharField('¿ Su casa cuenta con servicio de drenaje conectado a una red pública o a una fora séptica ?:', choices=comb, max_length=100)
    section5_obs = models.CharField('Observaciones', max_length=100, null=True, blank=False)
    punct_section5 = models.IntegerField('puntuación total obtenida en el apartado ')


    veracity = models.BooleanField(' ¿ Confirma que toda la informacion proporcionada es verídica ?', null=True, blank=True) 
    total_punct = models.IntegerField('puntuación total obtenida en  el ESE ')   # este dato  debe ser calculado a partir de los resultados de cada apartado
    porcent_punct = models.IntegerField('nivel de vulnerabilidad o pobreza obtenido  en  el Estudio Socio Económico (Porciento) ')
    poverty_level = models.IntegerField('nivel de vulnerabilidad o pobreza obtenido  en  el Estudio Socio Económico (Puntos)')
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Estudiante: ' + self.first_name + ' ' + self.first_last_name + ' ' + self.second_last_name
    

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
