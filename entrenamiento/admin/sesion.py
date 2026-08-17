from django.contrib import admin
from ..models import Sesion


@admin.register(Sesion)
class SesionAdmin(admin.ModelAdmin):

    list_display = ['practicante', 'fecha', 'duracion_min', 'dojo']
    list_filter = ['fecha', 'dojo']
    filter_horizontal = ('tecnicas',)