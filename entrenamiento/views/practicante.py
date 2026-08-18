from rest_framework import viewsets
from ..models import Practicante
from ..serializers import PracticanteSerializer


class PracticanteViewSet(viewsets.ModelViewSet):

    queryset = Practicante.objects.select_related('user', 'cinturon_actual').all()
    serializer_class = PracticanteSerializer