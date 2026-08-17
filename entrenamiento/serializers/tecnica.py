from rest_framework import serializers
from ..models import Tecnica


class TecnicaSerializer(serializers.ModelSerializer):

    # Campo calculado de solo-lectura: expone la etiqueta legible del choice
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)

    class Meta:
        model = Tecnica
        fields = ['id', 'nombre', 'categoria', 'categoria_display', 'cinturon_minimo']
    