from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError as DjangoValidationError
from ..models import Promocion
from ..serializers import PromocionSerializer
from ..permissions import PuedePromover


class PromocionViewSet(viewsets.ModelViewSet):

    queryset = Promocion.objects.all()
    serializer_class = PromocionSerializer
    permission_classes = [IsAuthenticated, PuedePromover]

    def perform_create(self, serializer):

        practicante = serializer.validate_data['practicante']
        cinturon_destino = serializer.validate_data['cinturon_hasta']
        otorgada_por = self.request.user.practicante

        try:
            promocion = practicante.promover_a(cinturon_destino, otorgada_por)
        except DjangoValidationError as e:
            # Traduce el error del modelo a un 400 con mensaje legible.
            raise serializer.ValidationError(e.messages)

        serializer.instance = promocion
    