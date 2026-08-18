from rest_framework import viewsets
from ..models import Tecnica
from ..serializers import TecnicaSerializer


class TecnicaViewSet(viewsets.ModelViewSet):
    queryset = Tecnica.objects.all()
    serializer_class = TecnicaSerializer