from rest_framework import serializers
from ..models import Promocion


class PromocionSerializer(serializers.ModelSerializer):

    class Meta:

        model = Promocion
        fields = ['id', 'practicante', 'cinturon_desde', 'cinturon_hasta', 'fecha', 'otorgada_por']