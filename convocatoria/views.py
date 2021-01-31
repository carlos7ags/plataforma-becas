from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from convocatoria.models import Convocatorias, Aspirantes
from becas.models import Student, StudentAcademicProgram, SocioEconomicStudy
from datetime import date
from django.urls import reverse_lazy
from convocatoria.forms import AspirantesForm
from bootstrap_modal_forms.generic import BSModalCreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect


class ConvocatoriasView(TemplateView):
    template_name = "convocatorias.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        convocatorias = Convocatorias.objects.all().order_by("-end_date")
        status = [
            convoc.start_date <= date.today() <= convoc.end_date
            for convoc in convocatorias
        ]
        registered = Aspirantes.objects.filter(username=self.request.user.id).all()
        registered = set([item.convocatoria.codigo for item in registered])
        active_convoc = [convoc.codigo for convoc in convocatorias]
        participated = [True if item in registered else False for item in active_convoc]

        context["convocatorias"] = zip(convocatorias, status, participated)
        context["complete_forms"] = self.check_complete_forms()
        return context

    def check_complete_forms(self):
        profile = Student.objects.filter(username=self.request.user.id).exists()
        program = StudentAcademicProgram.objects.filter(username=self.request.user.id).exists()
        socioeconomic = SocioEconomicStudy.objects.filter(username=self.request.user.id).exists()
        return profile and program and socioeconomic


class AspirantesCreateView(BSModalCreateView):
    template_name = 'register_aspirant.html'
    form_class = AspirantesForm
    success_message = 'Felicidades: Tu aplicación se registro con éxito.'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        convocatorias = Convocatorias.objects.all().order_by("-end_date")
        status = [
            convoc.start_date <= date.today() <= convoc.end_date
            for convoc in convocatorias
        ]
        context["convocatorias"] = zip(convocatorias, status)
        return context