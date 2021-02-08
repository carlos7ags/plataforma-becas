from django.forms import ModelForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Submit,
    Row,
    Column,
    HTML,
    Div,
    Button,
    MultiField,
    Reset,
)
from crispy_forms.bootstrap import (
    Accordion,
    Field,
    PrependedText,
    PrependedAppendedText,
)
from crispy_forms.bootstrap import AccordionGroup, FormActions, TabHolder, Tab

from becas.models import Student, StudentAcademicProgram, SocioEconomicStudy
from datetime import datetime
from crispy_forms.helper import FormHelper


class StudentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML("<h4>Información Personal</h4>"),
            Row(
                Column(Field("student_id"), css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("nombre"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("primer_apellido", css_class="form-group col-md-4 mb-1"),
                Column("segundo_apellido", css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("fecha_nacimiento", css_class="form-group col-md-4 mb-1"),
                Column("lugar_nacimiento", css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("ine", css_class="form-group col-md-4 mb-1"),
                Column("marital_status", css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("pic"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            HTML("<br><h4>Datos de Contacto</h4>"),
            Row(
                Column("calle", css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("numero_ext", css_class="form-group col-md-2 mb-1"),
                Column("numero_int", css_class="form-group col-md-2 mb-1"),
                Column("colonia", css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("cp", css_class="form-group col-md-2 mb-1"),
                Column("localidad", css_class="form-group col-md-3 mb-1"),
                Column("municipio", css_class="form-group col-md-3 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("telefono", css_class="form-group col-md-3 mb-1"),
                Column("celular", css_class="form-group col-md-3 mb-1"),
                css_class="form-row",
            ),
            FormActions(
                Submit("save", "Guardar"),
            ),
        )

    class Meta:
        model = Student
        exclude = ("validated",)
        widgets = {
            "fecha_nacimiento": forms.SelectDateWidget(
                years=range(datetime.now().year, 1900, -1),
                attrs=({"style": "width: 33%; display: inline-block;"}),
            ),
        }


class StudentAcademicProgramForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(Field("university"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("grado", css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("programa", css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("nivel_actual", css_class="form-group col-md-3 mb-1"),
                Column("promedio", css_class="form-group col-md-3 mb-1"),
                css_class="form-row",
            ),
            "continua",
            FormActions(
                Submit("save", "Guardar"),
            ),
        )

    class Meta:
        model = StudentAcademicProgram
        exclude = ("validated",)


class SocioEconomicStudyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML("<h4>Datos Generales</h4>"),
            Row(
                Column(Field("poverty_range"), css_class="form-group col-md-8 mb-1"),
            ),
            Row(
                Column(
                    Field("average_grade_range"), css_class="form-group col-md-4 mb-1"
                ),
                Column(Field("family_members"), css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            HTML("<h4>Datos Económicos</h4>"),
            Row(
                Column(
                    Field("family_monthly_income"), css_class="form-group col-md-4 mb-1"
                ),
                css_class="form-row",
            ),
            HTML("<h5>Fuentes de Ingreso</h5>"),
            Row(
                HTML('<h6 class="col-md-1">Padre</h6>'),
                Field("dad_occupation", wrapper_class="col-md-3"),
                PrependedAppendedText(
                    "dad_income", "$", ".00", wrapper_class="col-md-4"
                ),
                css_class="form-row",
            ),
            Row(
                HTML('<h6 class="col-md-1">Madre</h6>'),
                Field("mom_occupation", wrapper_class="col-md-3"),
                PrependedAppendedText(
                    "mom_income", "$", ".00", wrapper_class="col-md-4"
                ),
                css_class="form-row",
            ),
            Row(
                HTML('<h6 class="col-md-1">Hijo(s)</h6>'),
                Field("son_occupation", wrapper_class="col-md-3"),
                PrependedAppendedText(
                    "son_income", "$", ".00", wrapper_class="col-md-4"
                ),
                css_class="form-row",
            ),
            Row(
                HTML('<h6 class="col-md-1">Candidato</h6>'),
                Field("candidate_occupation", wrapper_class="col-md-3"),
                PrependedAppendedText(
                    "candidate_income", "$", ".00", wrapper_class="col-md-4"
                ),
                css_class="form-row",
            ),
            Row(
                HTML('<h6 class="col-md-1">Otros</h6>'),
                Field("other_occupation", wrapper_class="col-md-3"),
                PrependedAppendedText(
                    "other_income", "$", ".00", wrapper_class="col-md-4"
                ),
                css_class="form-row",
            ),
            HTML("<h5>Gasto Familiar</h5>"),
            Row(
                PrependedAppendedText("exp_food", "$", ".00", wrapper_class="col-md-4"),
                PrependedAppendedText("exp_rent", "$", ".00", wrapper_class="col-md-4"),
                PrependedAppendedText(
                    "exp_water", "$", ".00", wrapper_class="col-md-4"
                ),
                PrependedAppendedText(
                    "exp_energy", "$", ".00", wrapper_class="col-md-4"
                ),
                PrependedAppendedText(
                    "exp_leisure", "$", ".00", wrapper_class="col-md-4"
                ),
                PrependedAppendedText(
                    "exp_transport", "$", ".00", wrapper_class="col-md-4"
                ),
                PrependedAppendedText(
                    "exp_education", "$", ".00", wrapper_class="col-md-4"
                ),
                PrependedAppendedText(
                    "exp_telecom", "$", ".00", wrapper_class="col-md-4"
                ),
                PrependedAppendedText(
                    "exp_medic", "$", ".00", wrapper_class="col-md-4"
                ),
                PrependedAppendedText("exp_gas", "$", ".00", wrapper_class="col-md-4"),
                PrependedAppendedText(
                    "exp_vestido", "$", ".00", wrapper_class="col-md-4"
                ),
                PrependedAppendedText(
                    "exp_loans", "$", ".00", wrapper_class="col-md-4"
                ),
                PrependedAppendedText(
                    "exp_gasolina", "$", ".00", wrapper_class="col-md-4"
                ),
                PrependedAppendedText(
                    "exp_otros", "$", ".00", wrapper_class="col-md-4"
                ),
            ),
            HTML("<h4>Educación</h4>"),
            Row(
                Column(
                    Field("education_level_father"),
                    css_class="form-group col-md-4 mb-1",
                ),
                Column(
                    Field("education_level_mother"),
                    css_class="form-group col-md-4 mb-1",
                ),
                css_class="form-row",
            ),
            HTML("<h4>Salud y Seguridad Social</h4>"),
            Row(
                Column(Field("social_security"), css_class="form-group col-md-6 mb-1"),
            ),
            Row(
                Column(Field("provider_perks"), css_class="form-group col-md-6 mb-1"),
                css_class="form-row",
            ),
            HTML("<h4>Características y Servicios de la Vivienda</h4>"),
            Row(
                Column(Field("home_type"), css_class="form-group col-md-4 mb-1"),
                Column(Field("home_floor"), css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("home_ceil"), css_class="form-group col-md-4 mb-1"),
                Column(Field("home_walls"), css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("home_persons"), css_class="form-group col-md-4 mb-1"),
                Column(Field("service_water"), css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(
                    Field("service_electricity"), css_class="form-group col-md-4 mb-1"
                ),
                Column(Field("service_sewer"), css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("service_gas"), css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            FormActions(
                Submit("save", "Guardar"),
            ),
        )

    class Meta:
        model = SocioEconomicStudy
        exclude = (
            "validated",
            "priority",
            "comments",
        )
        widgets = {
            "dad_occupation": forms.TextInput(attrs={"placeholder": "Ocupación"}),
            "dad_income": forms.TextInput(attrs={"placeholder": "Ingreso mensual"}),
            "mom_occupation": forms.TextInput(attrs={"placeholder": "Ocupación"}),
            "mom_income": forms.TextInput(attrs={"placeholder": "Ingreso mensual"}),
            "son_occupation": forms.TextInput(attrs={"placeholder": "Ocupación"}),
            "son_income": forms.TextInput(attrs={"placeholder": "Ingreso mensual"}),
            "candidate_occupation": forms.TextInput(attrs={"placeholder": "Ocupación"}),
            "candidate_income": forms.TextInput(
                attrs={"placeholder": "Ingreso mensual"}
            ),
            "other_occupation": forms.TextInput(attrs={"placeholder": "Ocupación"}),
            "other_income": forms.TextInput(attrs={"placeholder": "Ingreso mensual"}),
            "exp_food": forms.TextInput(attrs={"placeholder": "Comida"}),
            "exp_rent": forms.TextInput(attrs={"placeholder": "Renta/Hipoteca"}),
            "exp_water": forms.TextInput(attrs={"placeholder": "Agua"}),
            "exp_energy": forms.TextInput(attrs={"placeholder": "Luz"}),
            "exp_leisure": forms.TextInput(attrs={"placeholder": "Diversión"}),
            "exp_transport": forms.TextInput(attrs={"placeholder": "Transporte"}),
            "exp_education": forms.TextInput(attrs={"placeholder": "Educación"}),
            "exp_telecom": forms.TextInput(
                attrs={"placeholder": "Teléfono/Cable/Internet"}
            ),
            "exp_medic": forms.TextInput(attrs={"placeholder": "Gastos médicos"}),
            "exp_gas": forms.TextInput(attrs={"placeholder": "Gas"}),
            "exp_vestido": forms.TextInput(attrs={"placeholder": "Vestido"}),
            "exp_loans": forms.TextInput(attrs={"placeholder": "Créditos"}),
            "exp_gasolina": forms.TextInput(attrs={"placeholder": "Gasolina"}),
            "exp_otros": forms.TextInput(attrs={"placeholder": "Otros"}),
        }
