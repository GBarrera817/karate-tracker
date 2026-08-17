from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Practicante


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class PracticanteSerializer(serializers.ModelSerializer):

    # Anida los datos del user en la respuesta, en vez de mostrar solo su id

    user = UserSerializer(read_only=True)
    rol_display = serializers.CharField(source='get_rol_display', read_only=True)

    class Meta:
        model = Practicante
        fields = ['id', 'user', 'rol', 'rol_display', 'cinturon_actual', 'fecha_ingreso']