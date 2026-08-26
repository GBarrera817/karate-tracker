from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Asistencia
from ..serializers import AsistenciaSerializer
from ..permissions import EscrituraSoloSensei


class AsistenciaViewSet(viewsets.ModelViewSet):

    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer
    permission_classes = [IsAuthenticated, EscrituraSoloSensei]