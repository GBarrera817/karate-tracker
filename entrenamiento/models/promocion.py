from django.db import models
from .practicante import Practicante
from .cinturon import Cinturon


class Promocion(models.Model):

    practicante = models.ForeignKey(Practicante, on_delete=models.CASCADE, related_name='promociones')
    cinturon_desde = models.ForeignKey(Cinturon, on_delete=models.PROTECT, related_name='promociones_desde', null=True, blank=True)
    cinturon_hasta = models.ForeignKey(Cinturon, on_delete=models.PROTECT, related_name='promociones_hasta')
    fecha = models.DateField(auto_now_add=True)
    otorgada_por = models.ForeignKey(
        Practicante,
        on_delete=models.SET_NULL,
        null=True,
        related_name='promociones_otorgadas'
    )

    class Meta:
        verbose_name = 'Promoción'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.practicante}: {self.cinturon_desde} → {self.cinturon_hasta}'