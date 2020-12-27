from django.shortcuts import render
from django.views.generic import TemplateView
from convocatoria.models import Convocatorias
from datetime import date


class ConvocatoriasView(TemplateView):
    template_name = "convocatorias.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        convocatorias = Convocatorias.objects.all().order_by("-end_date")
        status = [convoc.start_date <= date.today() <= convoc.end_date for convoc in convocatorias]
        context['convocatorias'] = zip(convocatorias, status)
        return context