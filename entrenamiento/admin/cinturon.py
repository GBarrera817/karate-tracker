from django.contrib import admin
from ..models import Cinturon


@admin.register(Cinturon)
class CinturonAdmin(admin.ModelAdmin):

    list_display = ("orden", "nombre", "sesiones_requeridas", "puede_promover", "puede_crear_tecnicas", 'color_hex') # 
    list_editable = ("puede_crear_tecnicas", "puede_promover")
    ordering = ('orden',)
