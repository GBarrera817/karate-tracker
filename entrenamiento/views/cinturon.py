from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Cinturon
from ..serializers import CinturonSerializer
from ..permissions import EscrituraSoloSensei


class CinturonViewSet(viewsets.ModelViewSet):

    queryset = Cinturon.objects.all()
    serializer_class = CinturonSerializer
    permission_classes = [IsAuthenticated, EscrituraSoloSensei]