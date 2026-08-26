from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Tecnica
from ..serializers import TecnicaSerializer
from ..permissions import PuedeGestionarTecnicas


class TecnicaViewSet(viewsets.ModelViewSet):
    queryset = Tecnica.objects.all()
    serializer_class = TecnicaSerializer
    permission_classes = [IsAuthenticated, PuedeGestionarTecnicas]