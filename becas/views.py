from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    RedirectView,
    UpdateView,
)
from django.urls import reverse_lazy
from becas.forms import StudentForm, StudentAcademicProgramForm
from django.urls import reverse
from becas.models import Student, Programs, StudentAcademicProgram
from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect


class StudentProfile(SuccessMessageMixin, CreateView):
    form_class = StudentForm
    template_name = "student_profile.html"
    success_url = reverse_lazy("dashboard")
    success_message = '¡Tu perfil se actualizó con éxito!'

    def form_valid(self, form):
        if form.is_valid:
            form.instance.username = self.request.user
            obj = form.save(commit=False)
            obj.save()
            return reverse("dashboard")


class StudentProfileUpdate(SuccessMessageMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "student_profile.html"
    success_url = reverse_lazy("dashboard")
    success_message = '¡Tu perfil se actualizó con éxito!'

    def user_passes_test(self, request):
        self.object = self.get_object()
        return self.object.username == request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect_to_login(request.get_full_path())
        return super(StudentProfileUpdate, self).dispatch(
            request, *args, **kwargs)


class UpdateStudentRedirectView(RedirectView):
    def get_redirect_url(self):
        if Student.objects.filter(username=self.request.user.id).exists():
            return reverse(
                "student-profile-update", kwargs={"pk": self.request.user.id}
            )
        else:
            return reverse("student-profile")


class StudentAcademicProgramView(SuccessMessageMixin,CreateView):
    form_class = StudentAcademicProgramForm
    template_name = "academic_program.html"
    success_url = reverse_lazy("dashboard")
    success_message = '¡Tu información académica se actualizó con éxito!'


    def form_valid(self, form):
        if form.is_valid:
            form.instance.username = self.request.user
            obj = form.save(commit=False)
            obj.save()
            return reverse("dashboard")


class StudentAcademicProgramUpdate(SuccessMessageMixin, UpdateView):
    model = StudentAcademicProgram
    form_class = StudentAcademicProgramForm
    template_name = "academic_program.html"
    success_url = reverse_lazy("dashboard")
    success_message = '¡Tu información académica se actualizó con éxito!'

    def user_passes_test(self, request):
        self.object = self.get_object()
        return self.object.username == request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect_to_login(request.get_full_path())
        return super(StudentProfileUpdate, self).dispatch(
            request, *args, **kwargs)


class UpdateStudentAcademicProgramRedirectView(RedirectView):
    def get_redirect_url(self):
        if Student.objects.filter(username=self.request.user.id).exists():
            return reverse(
                "academic-program-update", kwargs={"pk": self.request.user.id}
            )
        else:
            return reverse("academic-program")

def load_programs(request):
    university_id = request.GET.get('university_id')
    grado_id = request.GET.get('grado_id')
    if university_id and grado_id:
        programs = Programs.objects.filter(university=university_id, grado=grado_id).order_by('programa')
    else:
        programs = Programs.objects.none()
    return render(request, 'hr/load_program.html', {'programs': programs})