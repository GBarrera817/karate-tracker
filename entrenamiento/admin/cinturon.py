from django.contrib import admin
from ..models import Cinturon


@admin.register(Cinturon)
class CinturonAdmin(admin.ModelAdmin):

    list_display = ['orden', 'nombre', 'sesiones_requeridas', 'color_hex']
    ordering = ('orden',)