
from django.forms import ModelForm

from convocatoria.models import Aspirantes


class AspirantesForm(ModelForm):
    class Meta:
        model = Aspirantes
        fields = ()
