from django.db import models
from .practicante import Practicante
from .tecnica import Tecnica


class Sesion(models.Model):

    practicante = models.ForeignKey(Practicante, on_delete=models.CASCADE, related_name='sesiones')
    fecha = models.DateField()
    duracion_min = models.PositiveIntegerField(help_text='Duración en minutos')
    dojo = models.CharField(max_length=100, blank=True)
    notas = models.TextField(blank=True)
    tecnicas = models.ManyToManyField(Tecnica, related_name='sesiones', blank=True)

    class Meta:
        verbose_name = 'Sesión'
        verbose_name_plural = 'Sesiones'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.practicante} - {self.fecha}'