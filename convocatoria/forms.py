from convocatoria.models import Aspirantes
from bootstrap_modal_forms.forms import BSModalModelForm


class AspirantesForm(BSModalModelForm):
    class Meta:
        model = Aspirantes
        fields = ()
