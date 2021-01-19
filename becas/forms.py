from django.forms import ModelForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Div, Field
from becas.models import Student, StudentAcademicProgram, SocioEconomicStudy


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        widgets = {
           
            'fecha_nacimiento': forms.SelectDateWidget(years=range(1950, datetime.now().year + 1), attrs=({'style': 'width: 33%; display: inline-block;'})),
            
        }
        localized_fields = "__all__"
    
    
class StudentEditForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        widgets = {
           
            'fecha_nacimiento': forms.SelectDateWidget(years=range(1950, datetime.now().year + 1), attrs=({'style': 'width: 33%; display: inline-block;'})),
            
        }
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
