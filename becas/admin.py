from django.contrib import admin

from becas.models import (
    AverageGradeRanges,
    Estados,
    FamilyMembersRange,
    FamilyMonthlyIncome,
    Grados,
    HomeCeil,
    HomeFloor,
    HomePersons,
    HomeType,
    HomeWalls,
    MaritalStatus,
    Modalidades,
    Municipios,
    ParentsEducationLevel,
    PovertyRange,
    Programs,
    ProviderPerks,
    ServiceElectricity,
    ServiceGas,
    ServiceSewer,
    ServiceWater,
    SocialSecurity,
    SocioEconomicStudy,
    Student,
    StudentAcademicProgram,
    Universities,
)

admin.site.register(AverageGradeRanges)
admin.site.register(Estados)
admin.site.register(FamilyMembersRange)
admin.site.register(FamilyMonthlyIncome)
admin.site.register(Grados)
admin.site.register(HomeCeil)
admin.site.register(HomeFloor)
admin.site.register(HomePersons)
admin.site.register(HomeType)
admin.site.register(HomeWalls)
admin.site.register(MaritalStatus)
admin.site.register(Modalidades)
admin.site.register(Municipios)
admin.site.register(ParentsEducationLevel)
admin.site.register(PovertyRange)
admin.site.register(Programs)
admin.site.register(ProviderPerks)
admin.site.register(ServiceElectricity)
admin.site.register(ServiceGas)
admin.site.register(ServiceSewer)
admin.site.register(ServiceWater)
admin.site.register(SocialSecurity)
admin.site.register(SocioEconomicStudy)
admin.site.register(Student)
admin.site.register(StudentAcademicProgram)
admin.site.register(Universities)

from import_export import resources
from import_export.admin import ImportExportModelAdmin


# ToDo: Crear dos clases como está para cada menu que queramos descargar a excel


class StudentResource(resources.ModelResource):
    class Meta:
        model = Student


class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource


class SocioEconomicStudyResource(resources.ModelResource):
    class Meta:
        model = SocioEconomicStudy


class SocioEconomicStudyAdmin(ImportExportModelAdmin):
    resource_class = SocioEconomicStudyResource


class StudentAcademicProgramResource(resources.ModelResource):
    class Meta:
        model = SocioEconomicStudy


class StudentAcademicProgramAdmin(ImportExportModelAdmin):
    resource_class = StudentAcademicProgramResource
