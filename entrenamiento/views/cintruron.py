from rest_framework import viewsets
from ..models import Cinturon
from ..serializers import CinturonSerializer


class CinturonViewSet(viewsets.ModelViewSet):

    queryset = Cinturon.objects.all()
    serializer_class = CinturonSerializer