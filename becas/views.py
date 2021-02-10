from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, RedirectView, TemplateView,
                                  UpdateView, View)
from xhtml2pdf import pisa
from io import BytesIO

from becas.forms import (SocioEconomicStudyForm, StudentAcademicProgramForm,
                         StudentForm)
from becas.models import (Programs, SocioEconomicStudy, Student,
                          StudentAcademicProgram)
from convocatoria.models import Aspirantes


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student"] = self.request.user in [
            student.username for student in Student.objects.all()
        ]
        context["program"] = self.request.user in [
            student.username for student in StudentAcademicProgram.objects.all()
        ]
        context["socioeconomico"] = self.request.user in [
            student.username for student in SocioEconomicStudy.objects.all()
        ]
        calls = Aspirantes.objects.filter(username=self.request.user.id)
        if calls:
            context["active_calls"] = True
            context["calls"] = calls
        else:
            context["active_calls"] = False
        return context


class StudentProfile(CreateView):
    form_class = StudentForm
    template_name = "student_profile.html"
    success_url = reverse_lazy("dashboard")

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.username = self.request.user
            obj.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {"form": form})


class StudentProfileUpdate(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "student_profile.html"
    success_url = reverse_lazy("dashboard")

    def user_passes_test(self, request):
        self.object = self.get_object()
        return self.object.username == request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect_to_login(request.get_full_path())
        return super(StudentProfileUpdate, self).dispatch(request, *args, **kwargs)


class UpdateStudentRedirectView(RedirectView):
    def get_redirect_url(self):
        if Student.objects.filter(username=self.request.user.id).exists():
            return reverse(
                "student-profile-update", kwargs={"pk": self.request.user.id}
            )
        else:
            return reverse("student-profile")


class StudentAcademicProgramView(CreateView):
    form_class = StudentAcademicProgramForm
    template_name = "academic_program.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        if form.is_valid:
            form.instance.username = self.request.user
            obj = form.save(commit=False)
            obj.save()
            return redirect("dashboard")


class StudentAcademicProgramUpdate(UpdateView):
    model = StudentAcademicProgram
    form_class = StudentAcademicProgramForm
    template_name = "academic_program.html"
    success_url = reverse_lazy("dashboard")

    def user_passes_test(self, request):
        self.object = self.get_object()
        return self.object.username == request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect_to_login(request.get_full_path())
        return super(StudentAcademicProgramUpdate, self).dispatch(
            request, *args, **kwargs
        )


class UpdateStudentAcademicProgramRedirectView(RedirectView):
    def get_redirect_url(self):
        if StudentAcademicProgram.objects.filter(
            username=self.request.user.id
        ).exists():
            return reverse(
                "academic-program-update", kwargs={"pk": self.request.user.id}
            )
        else:
            return reverse("academic-program")


def load_programs(request):
    university_id = request.GET.get("university_id")
    grado_id = request.GET.get("grado_id")
    if university_id and grado_id:
        programs = Programs.objects.filter(
            university=university_id, grado=grado_id
        ).order_by("programa")
    else:
        programs = Programs.objects.none()
    return render(request, "hr/load_program.html", {"programs": programs})


class SocioEconomicStudyView(CreateView):
    form_class = SocioEconomicStudyForm
    template_name = "socio_economic_study.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        if form.is_valid:
            form.instance.username = self.request.user
            obj = form.save(commit=False)
            obj.save()
            return redirect("dashboard")


class SocioEconomicStudyUpdate(UpdateView):
    model = SocioEconomicStudy
    form_class = SocioEconomicStudyForm
    template_name = "socio_economic_study.html"
    success_url = reverse_lazy("dashboard")

    def user_passes_test(self, request):
        self.object = self.get_object()
        return self.object.username == request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect_to_login(request.get_full_path())
        return super(SocioEconomicStudyUpdate, self).dispatch(request, *args, **kwargs)


class UpdateSocioEconomicStudyRedirectView(RedirectView):
    def get_redirect_url(self):
        if SocioEconomicStudy.objects.filter(username=self.request.user.id).exists():
            return reverse(
                "socio-economic-study-update", kwargs={"pk": self.request.user.id}
            )
        else:
            return reverse("socio-economic-study")


class ConstanciaPdfView(View):
    def get(self, request, *args, **kwargs):
        template_path = "solictud.html"
        context = {}
        context["student"] = Student.objects.filter(username=self.request.user).first()
        context["academic"] = StudentAcademicProgram.objects.filter(
            username=self.request.user
        ).first()
        context["aspirante"] = Aspirantes.objects.filter(
            username=self.request.user
        ).first()

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="constancia.pdf"'
        template = get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse("We had some errors <pre>" + html + "</pre>")
        return response


class EsePdfView(View):
    def get(self, request, *args, **kwargs):
        template_path = "ese.html"
        context = {}
        context["student"] = Student.objects.filter(username=self.request.user).first()
        context["ese"] = SocioEconomicStudy.objects.filter(
            username=self.request.user
        ).first()
        context["academic"] = StudentAcademicProgram.objects.filter(
            username=self.request.user
        ).first()

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="ese.pdf"'
        template = get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse("We had some errors <pre>" + html + "</pre>")
        return response


class SolicitudPdfView(View):
    def get(self, request, *args, **kwargs):
        template = get_template('solicitud.html')
        context = {}
        context["student"] = Student.objects.filter(username=self.request.user).first()
        context["academic"] = StudentAcademicProgram.objects.filter(
            username=self.request.user
        ).first()
        context["ese"] = SocioEconomicStudy.objects.filter(
            username=self.request.user
        ).first()

        html = template.render(context)
        pdf = render_to_pdf('solicitud.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "solicitud.pdf"
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None