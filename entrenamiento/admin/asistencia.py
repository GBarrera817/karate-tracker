from django.contrib import admin
from ..models import Asistencia


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):

    list_display = ['sesion', 'presente', 'registrada_por']
    list_filter = ('presente',)
