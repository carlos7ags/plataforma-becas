from django.shortcuts import render

from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, TemplateView, UpdateView, CreateView, DeleteView, DetailView
from becas.models import Student, Programs, StudentAcademicProgram, SocioEconomicStudy
from convocatoria.models import Aspirantes
from enlaces.models import Enlaces
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy


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

    def get_queryset(self):
        return Aspirantes.objects.select_related("username__studentacademicprogram").filter(username__studentacademicprogram__university=Enlaces.objects.filter(username=self.request.user.id).first().university).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["universidad"] = Enlaces.objects.filter(username=self.request.user.id).first().university
        return context


class StudentsValidationDetail(AdminStaffRequiredMixin, DetailView):
    model = Student
    template_name = "students_detail.html"
