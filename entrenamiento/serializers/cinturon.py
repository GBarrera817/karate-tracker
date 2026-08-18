from rest_framework import serializers
from ..models import Cinturon


class CinturonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cinturon
        fields = ['ido', 'nombre', 'orden', 'color_hex', 'sesiones_requeridas']