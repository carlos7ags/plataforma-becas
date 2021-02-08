from django.contrib import admin

from convocatoria.models import Aspirantes, Convocatorias, Modalidades

admin.site.register(Aspirantes)
admin.site.register(Convocatorias)
admin.site.register(Modalidades)


from import_export import resources
from import_export.admin import ImportExportModelAdmin

# ToDo: Crear dos clases como está para cada menu que queramos descargar a excel


class AspirantesResource(resources.ModelResource):
    class Meta:
        model = Aspirantes


class AspirantesAdmin(ImportExportModelAdmin):
    resource_class = AspirantesResource
