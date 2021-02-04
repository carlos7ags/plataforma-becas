from django.shortcuts import render

from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, TemplateView
from becas.models import Student
from enlaces.models import Enlaces
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class DashboardEnlacesView(AdminStaffRequiredMixin, TemplateView):
    template_name = "dashboard_enlaces.html"


"""
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
"""


class ProgramasUpdate(AdminStaffRequiredMixin, TemplateView):
    template_name = "dashboard_enlaces.html"


class StudentsValidationList(AdminStaffRequiredMixin, ListView):
    context_object_name = "students_list"
    template_name = "students_list.html"
    paginate_by = 10
    ordering = ["-validated", "username"]

    def get_queryset(self):
        return Student.objects.select_related("username__studentacademicprogram").filter(username__studentacademicprogram__university=Enlaces.objects.filter(username=self.request.user.id).first().university).all()

