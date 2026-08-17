from django.contrib import admin
from ..models import Practicante


@admin.register(Practicante)
class PracticanteAdmin(admin.ModelAdmin):

    list_display = ['user', 'rol', 'cinturon_actual', 'fecha_ingreso']
    list_filter = ['rol', 'cinturon_actual']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
