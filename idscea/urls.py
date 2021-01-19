from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.views.generic import TemplateView
from accounts.views import UserRegistrationView
import django.contrib.auth.views as auth_views
from django.contrib.auth.decorators import login_required
from becas.views import StudentProfile, StudentProfileUpdate, UpdateStudentRedirectView, StudentAcademicProgramView, StudentAcademicProgramUpdate, UpdateStudentAcademicProgramRedirectView, load_programs, DashboardView, SocioEconomicStudyView, SocioEconomicStudyUpdate, UpdateSocioEconomicStudyRedirectView
from convocatoria.views import ConvocatoriasView


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='base.html'), name='home'),

    url(r'^new-user/$', UserRegistrationView.as_view(), name='user_registration'),
    path('register/done/', TemplateView.as_view(template_name="register_done.html"), name='register_done'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    url(r'^password_change/$', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html'), name='password_change'),
    url(r'password_change/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),


    path('dashboard/', login_required(DashboardView.as_view()), name='dashboard'),

    path('convocatorias/', login_required(ConvocatoriasView.as_view()), name='convocatorias'),

    path('profile/', login_required(StudentProfile.as_view()), name='student-profile'),
    url(r'profile/(?P<pk>\d+)/update/$', login_required(StudentProfileUpdate.as_view()), name='student-profile-update'),
    path('profile/redirect', login_required(UpdateStudentRedirectView.as_view()), name='student-profile-redirect'),

    path('economic/', login_required(SocioEconomicStudyView.as_view()), name='socio-economic-study'),
    url(r'economic/(?P<pk>\d+)/update/$', login_required(SocioEconomicStudyUpdate.as_view()), name='socio-economic-study-update'),
    path('economic/redirect', login_required(UpdateSocioEconomicStudyRedirectView.as_view()), name='socio-economic-study-redirect'),

    path('academic/', login_required(StudentAcademicProgramView.as_view()), name='academic-program'),
    url(r'academic/(?P<pk>\d+)/update/$', login_required(StudentAcademicProgramUpdate.as_view()), name='academic-program-update'),
    path('academic/redirect', login_required(UpdateStudentAcademicProgramRedirectView.as_view()), name='academic-program-redirect'),
    path('ajax/load-programs/', load_programs, name='ajax-load-programs'),

]