from rest_framework import serializers
from ..models import Promocion


class PromocionSerializer(serializers.ModelSerializer):

    otorgada_por = serializers.PrimaryKeyRelatedField(read_only=True)
    cinturon_desde = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:

        model = Promocion
        fields = ['id', 'practicante', 'cinturon_desde', 'cinturon_hasta', 'fecha', 'otorgada_por']