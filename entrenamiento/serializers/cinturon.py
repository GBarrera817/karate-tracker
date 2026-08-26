from rest_framework import serializers
from ..models import Cinturon


class CinturonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cinturon
        fields = [
            'id',
            'nombre',
            'orden',
            'color_hex',
            'sesiones_requeridas',
            # 'puede_crear_tecnicas',
            # 'puede_promover'
            'otorga_autoridad',
        ]