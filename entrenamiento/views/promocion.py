from rest_framework import viewsets
from ..models import Promocion
from ..serializers import PromocionSerializer


class PromocionViewSet(viewsets.ModelViewSet):
    queryset = Promocion.objects.all()
    serializer_class = PromocionSerializer