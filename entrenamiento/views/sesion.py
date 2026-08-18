from rest_framework import viewsets
from ..models import Sesion
from ..serializers import SesionSerializer


class SesionViewSet(viewsets.ModelViewSet):

    queryset = Sesion.objects.select_related('practicante').prefetch_related('tecnicas').all()
    serializer_class = SesionSerializer