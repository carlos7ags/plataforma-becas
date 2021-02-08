from convocatoria.models import Aspirantes
from bootstrap_modal_forms.forms import BSModalModelForm
from django.forms import ModelForm
from bootstrap_modal_forms.mixins import CreateUpdateAjaxMixin
from convocatoria.models import Convocatorias
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


class AspirantesForm(ModelForm):
    class Meta:
        model = Aspirantes
        fields = ()
