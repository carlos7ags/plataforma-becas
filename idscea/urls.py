import django.contrib.auth.views as auth_views
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView

from accounts.views import UserRegistrationView
from becas.views import (ConstanciaPdfView, DashboardView, EsePdfView,
                         SocioEconomicStudyUpdate, SocioEconomicStudyView,
                         SolicitudPdfView, StudentAcademicProgramUpdate,
                         StudentAcademicProgramView, StudentProfile,
                         StudentProfileUpdate,
                         UpdateSocioEconomicStudyRedirectView,
                         UpdateStudentAcademicProgramRedirectView,
                         UpdateStudentRedirectView, load_programs)
from convocatoria.views import ConvocatoriasView, aspirante_create
from enlaces.views import (DashboardEnlacesView, ProgramsCreate,
                           ProgramsDelete, ProgramsList, ProgramsUpdate,
                           StudentsValidationDetail, StudentsValidationList)

urlpatterns = [
    path("admin/", admin.site.urls),
    url(r"^$", TemplateView.as_view(template_name="home.html"), name="home"),
    url(r"^new-user/$", UserRegistrationView.as_view(), name="user_registration"),
    path(
        "register/done/",
        TemplateView.as_view(template_name="register_done.html"),
        name="register_done",
    ),
    url(
        r"^login/$",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    url(r"^logout/$", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    url(
        r"^password_change/$",
        auth_views.PasswordChangeView.as_view(
            template_name="password_change_form.html"
        ),
        name="password_change",
    ),
    url(
        r"password_change/done/$",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("dashboard/", login_required(DashboardView.as_view()), name="dashboard"),
    path(
        "convocatorias/",
        login_required(ConvocatoriasView.as_view()),
        name="convocatorias",
    ),
    url(
        r"convocatorias/(?P<convocCode>[a-zA-Z0-9]+)/$",
        login_required(aspirante_create),
        name="create-aspirante",
    ),
    path("profile/", login_required(StudentProfile.as_view()), name="student-profile"),
    url(
        r"profile/(?P<pk>\d+)/update/$",
        login_required(StudentProfileUpdate.as_view()),
        name="student-profile-update",
    ),
    path(
        "profile/redirect",
        login_required(UpdateStudentRedirectView.as_view()),
        name="student-profile-redirect",
    ),
    path(
        "economic/",
        login_required(SocioEconomicStudyView.as_view()),
        name="socio-economic-study",
    ),
    url(
        r"economic/(?P<pk>\d+)/update/$",
        login_required(SocioEconomicStudyUpdate.as_view()),
        name="socio-economic-study-update",
    ),
    path(
        "economic/redirect",
        login_required(UpdateSocioEconomicStudyRedirectView.as_view()),
        name="socio-economic-study-redirect",
    ),
    path(
        "academic/",
        login_required(StudentAcademicProgramView.as_view()),
        name="academic-program",
    ),
    url(
        r"academic/(?P<pk>\d+)/update/$",
        login_required(StudentAcademicProgramUpdate.as_view()),
        name="academic-program-update",
    ),
    path(
        "academic/redirect",
        login_required(UpdateStudentAcademicProgramRedirectView.as_view()),
        name="academic-program-redirect",
    ),
    path("ajax/load-programs/", load_programs, name="ajax-load-programs"),
    path(
        "enlaces/",
        login_required(DashboardEnlacesView.as_view()),
        name="dashboard-enlaces",
    ),
    path(
        "enlaces/programs/list",
        login_required(ProgramsList.as_view()),
        name="programs-list",
    ),
    url(
        r"programs/(?P<pk>\d+)/update/$",
        login_required(ProgramsUpdate.as_view()),
        name="programs-update",
    ),
    path(
        "enlaces/programs/create",
        login_required(ProgramsCreate.as_view()),
        name="programs-create",
    ),
    path(
        "enlaces/programs/delete/<str:username>",
        login_required(ProgramsDelete.as_view()),
        name="programs-delete",
    ),
    path(
        "enlaces/student_validation",
        login_required(StudentsValidationList.as_view()),
        name="student-validation",
    ),
    path(
        "enlaces/aspirant/<int:pk>",
        login_required(StudentsValidationDetail.as_view()),
        name="aspirant-view",
    ),
    path(
        "generate_constancia/", ConstanciaPdfView.as_view(), name="constancia-print-pdf"
    ),
    path("generate_solicitud/", SolicitudPdfView.as_view(), name="solicitud-print-pdf"),
    path("generate_ese/", EsePdfView.as_view(), name="ese-print-pdf"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
