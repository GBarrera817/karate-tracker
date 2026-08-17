from django.db import models
from .sesion import Sesion
from .practicante import Practicante


class Asistencia(models.Model):

    sesion = models.OneToOneField(Sesion, on_delete=models.CASCADE, related_name='asistencia')
    presente = models.BooleanField(default=True)
    registrada_por = models.ForeignKey(
        Practicante,
        on_delete=models.SET_NULL,
        null=True,
        related_name='asistencias_registradas',
        help_text='Instructor que registró la asistencia'
    )

    def __str__(self):
        estado = 'Presente' if self.presente else 'Ausente'
        return f'{self.sesion} - {estado}'