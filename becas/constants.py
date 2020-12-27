CIVIL = (
    ("0", "Soltera/o"),
    ("1", "Casada/o"),
    ("2", "Viuda/o"),
    ("3", "Divorciada/o"),
    ("4", "Separada/o"),
)

SI = (("0", "No"), ("1", "Sí"))

SI1 = (("0", "No"), ("1", "Sí"))

VIVE = (("0", "Con padres o tutores"), ("1", "Con familiares"), ("2", "Sola/o"))

CASA = (("0", "Propia"), ("1", "Rentada"))

universidad = [
    "Universidad Autónoma de Aguascalientes",
    "Universidad Tecnológica de Aguascalientes",
    "Universidad Tecnológica El Retoño",
    "Universidad Tecnológica de Calvillo",
    "Universidad Tecnológica del Norte de Aguascalientes",
    "Universidad Politécnica de Aguascalientes",
    "Universidad de las Artes",
    "Universidad Tecnológica Metropolitana de Aguascalientes",
    "Instituto Tecnológico El Llano",
    "Instituto Tecnológico de Pabellón de Arteaga",
    "Instituto Tecnológico de Aguascalientes",
]
UNIVERSIDAD = [(str(i), j) for i, j in zip(range(len(universidad)), universidad)]

SEMESTRE = (("0", "Semestral"), ("1", "Cuatrimestral"))

NIVEL = (
    ("0", "Técnico Superior Universitario"),
    ("1", "Licenciatura"),
    ("2", "Ingenieria"),
)

MOD_BECA = (("0", "Formación"), ("1", "Estancia Académica"))
