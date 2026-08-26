from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Sesion
from ..serializers import SesionSerializer


class SesionViewSet(viewsets.ModelViewSet):

    serializer_class = SesionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Sesion.objects.select_related('practicante').prefetch_related('tecnicas')
        practicante = getattr(self.request.user, 'practicante', None)

        if practicante is None:
            return qs.none()

        if practicante.rol == practicante.SENSEI:
            return qs  # sensei ve todas

        return qs.filter(practicante=practicante)  # alumno ve solo las suyas

    def perform_create(self, serializer):

        # La sesión se atribuye a quien la registra: un alumno no puede crear
        serializer.save(practicante=self.request.user.practicante)
