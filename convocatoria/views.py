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
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from becas.models import (PovertyRange, AverageGradeRanges, FamilyMembersRange, FamilyMonthlyIncome, ParentsEducationLevel, ParentsEducationLevel, SocialSecurity, ProviderPerks, HomeType, HomeFloor, HomeCeil, HomeWalls,
HomePersons, ServiceWater, ServiceElectricity, ServiceSewer, ServiceGas,)

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


def aspirante_create(request, convocCode):
    data = dict()
    if request.method == 'POST':
        form = AspirantesForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.username = request.user
            last_id = Aspirantes.objects.all().order_by("-id").first()
            obj.id = last_id.id + 1 if last_id else 27
            obj.convocatoria = Convocatorias.objects.filter(codigo=convocCode).first()
            obj.folio = convocCode + str(obj.id + 20210000)
            obj.socioeconomic_score = get_socio_economic_result(request.user)
            obj.grade = StudentAcademicProgram.objects.filter(username=request.user).first().promedio
            obj.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = AspirantesForm()

    context = {'form': form,
               'convocCode': convocCode}
    data['html_form'] = render_to_string('register_aspirant.html',
        context,
        request=request
    )
    return JsonResponse(data)


def get_socio_economic_result(username):
    return 0

"""
    answers = StudentAcademicProgram.objects.filter(username=username).first()
    elements = {
    "poverty_range": PovertyRange,
    "average_grade_range": AverageGradeRanges,
    "family_members": FamilyMembersRange,
    "family_monthly_income": FamilyMonthlyIncome,
    "education_level_father": ParentsEducationLevel,
    "education_level_mother": ParentsEducationLevel,
    "social_security": SocialSecurity,
    "provider_perks": ProviderPerks,
    "home_type": HomeType,
    "home_floor": HomeFloor,
    "home_ceil": HomeCeil,
    "home_walls": HomeWalls,
    "home_persons": HomePersons,
    "service_water": ServiceWater,
    "service_electricity": ServiceElectricity,
    "service_sewer": ServiceSewer,
    "service_gas": ServiceGas,
    }
    for key, elem in elements:
        answers[elem]

"""
