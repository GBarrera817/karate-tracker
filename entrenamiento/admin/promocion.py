from django.contrib import admin
from ..models import Promocion


@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ['practicante', 'cinturon_desde', 'cinturon_hasta', 'fecha', 'otorgada_por']
    list_filter = ('fecha',)