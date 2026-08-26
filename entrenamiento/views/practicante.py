from rest_framework import viewssets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Practicante
from ..serializers import PracticanteSerializer


class PracticanteViewSet(viewsets.ModelViewSet):

    queryset = Practicante.objects.select_related('user', 'cinturon_actual').all()
    serializer_class = PracticanteSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        practicante = self.get_object()

        return Response(practicante.estadisticas_apoyo()))