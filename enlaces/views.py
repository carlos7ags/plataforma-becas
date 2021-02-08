from django.shortcuts import render

from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, TemplateView, UpdateView, CreateView, DeleteView, DetailView
from becas.models import Student, Programs, StudentAcademicProgram, SocioEconomicStudy
from convocatoria.models import Aspirantes
from enlaces.models import Enlaces
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User



class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class DashboardEnlacesView(AdminStaffRequiredMixin, TemplateView):
    template_name = "dashboard_enlaces.html"


class ProgramsList(AdminStaffRequiredMixin, ListView):
    template_name = "programs_list.html"
    paginate_by = 10
    ordering = ["grado", "programa"]

    def get_queryset(self):
        return Programs.objects.filter(university=Enlaces.objects.filter(username=self.request.user.id).first().university).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["universidad"] = Enlaces.objects.filter(username=self.request.user.id).first().university
        return context

class ProgramsCreate(AdminStaffRequiredMixin, CreateView):
    model = Programs
    template_name = "programs_create.html"
    success_url = reverse_lazy('programs-list')
    fields = '__all__'

class ProgramsUpdate(AdminStaffRequiredMixin, UpdateView):
    model = Programs
    template_name = "programs_update.html"
    success_url = reverse_lazy('programs-list')
    fields = '__all__'


class ProgramsDelete(AdminStaffRequiredMixin, DeleteView):
    model = Programs
    success_url = reverse_lazy('programs-list')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class StudentsValidationList(AdminStaffRequiredMixin, ListView):
    context_object_name = "students_list"
    template_name = "students_list.html"
    paginate_by = 25
    ordering = ["username"]

    """        aspirant_usernames = Aspirantes.objects.all().values_list("username__username", flat=True)

            all_aspirants = User.objects.filter(username__in=aspirant_usernames).select_related("studentacademicprogram").filter(
                studentacademicprogram__university=enlace_universidad).select_related("student")
            print(all_aspirants.values())"""

    def get_queryset(self):
        enlace_universidad = Enlaces.objects.filter(username=self.request.user.id).first().university
        all_aspirants = Aspirantes.objects.select_related("username__studentacademicprogram").filter(
            username__studentacademicprogram__university=enlace_universidad).select_related("username__student").order_by('validated', 'username').all()
        return all_aspirants

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["universidad"] = Enlaces.objects.filter(username=self.request.user.id).first().university
        return context


class StudentsValidationDetail(AdminStaffRequiredMixin, UpdateView):
    model = Aspirantes
    template_name = "students_detail.html"
    success_url = reverse_lazy('student-validation')
    fields = ["prioritario", "comments", "validated"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = Student.objects.filter(username=self.object.username).first()
        context['ses'] = SocioEconomicStudy.objects.filter(username=self.object.username).first()
        context['academic'] = StudentAcademicProgram.objects.filter(username=self.object.username).first()
        context['email'] = User.objects.filter(username=self.object.username).first().email
        tel = "(%c%c%c)-%c%c%c-%c%c%c%c" % tuple(context['student'].telefono)
        cel = "(%c%c%c)-%c%c%c-%c%c%c%c" % tuple(context['student'].celular)
        context['telefonos'] = "Teléfono: " + tel + ", Celular: " + cel
        return context
