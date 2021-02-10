from datetime import date

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from becas.models import (
    AverageGradeRanges,
    FamilyMembersRange,
    FamilyMonthlyIncome,
    HomeCeil,
    HomeFloor,
    HomePersons,
    HomeType,
    HomeWalls,
    ParentsEducationLevel,
    PovertyRange,
    ProviderPerks,
    ServiceElectricity,
    ServiceGas,
    ServiceSewer,
    ServiceWater,
    SocialSecurity,
    SocioEconomicStudy,
    Student,
    StudentAcademicProgram,
)
from convocatoria.forms import AspirantesForm
from convocatoria.models import Aspirantes, Convocatorias


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
        program = StudentAcademicProgram.objects.filter(
            username=self.request.user.id
        ).exists()
        socioeconomic = SocioEconomicStudy.objects.filter(
            username=self.request.user.id
        ).exists()
        return profile and program and socioeconomic


def aspirante_create(request, convocCode):
    data = dict()
    if request.method == "POST":
        form = AspirantesForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.username = request.user
            last_id = Aspirantes.objects.all().order_by("-id").first()
            obj.id = last_id.id + 1 if last_id else 27
            obj.convocatoria = Convocatorias.objects.filter(codigo=convocCode).first()
            obj.folio = convocCode + str(obj.id + 20210000)
            obj.socioeconomic_score = get_socio_economic_result(username=request.user)
            obj.valor_beca = get_costo_beca(username=request.user)
            obj.grade = (
                StudentAcademicProgram.objects.filter(username=request.user)
                .first()
                .promedio
            )
            obj.save()
            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    else:
        form = AspirantesForm()

    context = {"form": form, "convocCode": convocCode}
    data["html_form"] = render_to_string(
        "register_aspirant.html", context, request=request
    )
    return JsonResponse(data)


def get_costo_beca(username):
    info_academ = (
        StudentAcademicProgram.objects.filter(username=username)
        .select_related("programa")
        .values_list("programa__duracion", "nivel_actual", "programa__costo")[0]
    )
    return (1 + info_academ[0] - info_academ[1]) * info_academ[2]


def get_socio_economic_result(username):
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

    accum = 0.0
    for key in elements.keys():
        accum += (
            SocioEconomicStudy.objects.filter(username=username)
            .select_related(key)
            .values_list(key, flat=True)[0]
        )

    if accum > 40:
        return 5
    elif accum > 30:
        return 4
    elif accum > 20:
        return 3
    elif accum > 10:
        return 2
    else:
        return 1
