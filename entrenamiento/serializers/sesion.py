from rest_framework import serializers
from ..models import Sesion


class SesionSerializer(serializers.ModelSerializer):

    practicante = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:

        model = Sesion
        fields = ['id', 'practicante', 'fecha', 'duracion_min', 'dojo', 'notas', 'tecnicas']