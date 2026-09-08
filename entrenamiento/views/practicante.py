from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Practicante
from ..serializers import PracticanteSerializer
from ..permissions import EscrituraSoloSensei


class PracticanteViewSet(viewsets.ModelViewSet):

    queryset = Practicante.objects.select_related('user', 'cinturon_actual').all()
    serializer_class = PracticanteSerializer
    permission_classes = [IsAuthenticated, EscrituraSoloSensei]

    @action(detail=False, methods=['get'])
    def yo(self, request):
        """Devuelve el practicante asociado al usuario autenticado."""

        practicante = getattr(request.user, 'practicante', None)

        if practicante is None:
            return Response({'detail': 'El usuario no tiene practicante asociado.'})

        serializer = self.get_serializer(practicante)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        practicante = self.get_object()

        return Response(practicante.estadisticas_apoyo())