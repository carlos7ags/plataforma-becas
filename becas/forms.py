from django.forms import ModelForm
from django import forms
from becas.models import Student, StudentAcademicProgram, SocioEconomicStudy


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        widgets = (
            {
                "fecha_nacimiento": forms.DateInput(
                    format=("%d/%m/%Y"),
                    attrs={"class": "form-control", "lang": "es", "type": "date"},
                ),
            },
        )
        localized_fields = "__all__"


class StudentEditForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        widgets = (
            {
                "fecha_nacimiento": forms.DateInput(
                    format=("%d/%m/%Y"),
                    attrs={"class": "form-control", "lang": "es", "type": "date"},
                ),
            },
        )
        localized_fields = "__all__"


class StudentAcademicProgramForm(ModelForm):
    class Meta:
        model = StudentAcademicProgram
        fields = "__all__"
        localized_fields = "__all__"


class SocioEconomicStudyForm(ModelForm):
    class Meta:
        model = SocioEconomicStudy
        fields = "__all__"


class SocioEconomicStudyEditForm(ModelForm):
    class Meta:
        model = SocioEconomicStudy
        fields = "__all__"
        localized_fields = "__all__"
