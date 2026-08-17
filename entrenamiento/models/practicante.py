from django.db import models
from django.contrib.auth.models import User
from .cinturon import Cinturon


class Practicante(models.Model):

    ALUMNO = 'alumno'
    SENSEI = 'sensei'
    ROL_CHOICES = [
        (ALUMNO, 'Alumno'),
        (SENSEI, 'Sensei')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='practicante')
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default=ALUMNO)
    cinturon_actual = models.ForeignKey(
        Cinturon,
        on_delete=models.PROTECT,
        related_name='practicante',
        null=True,
        blank=True
    )
    fecha_ingreso = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} ({self.get_rol_display()})'
    