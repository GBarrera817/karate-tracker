from django.contrib import admin
from ..models import Tecnica


@admin.register(Tecnica)
class TecnicaAdmin(admin.ModelAdmin):

    list_display = ['nombre', 'categoria', 'cinturon_minimo']
    list_filter = ['categoria', 'cinturon_minimo']
    search_fields = ('nombre',)