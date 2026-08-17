from django.db import models
from .cinturon import Cinturon


class Tecnica(models.Model):
    KIHON = 'kihon'
    KATA = 'kata'
    KUMITE = 'kumite'
    IDO_GEIKO = 'ido_geiko'
    DACHI = 'dachi'
    TSUKI = 'tsuki'
    UCHI = 'uchi'
    UKE = 'uke'
    GERI = 'geri'
    CATEGORIA_CHOICES = [
        (KIHON, 'Kihon'),
        (KATA, 'Kata'),
        (KUMITE, 'Kumite'),
        (IDO_GEIKO, 'Ido Geiko'),
        (DACHI, 'Dachi'),
        (TSUKI, 'Tsuki'),
        (UCHI, 'Uchi'),
        (UKE, 'Uke'),
        (GERI, 'Geri')
    ]

    nombre = models.CharField(max_length=150, unique=True)
    categoria = models.CharField(max_length=10, choices=CATEGORIA_CHOICES)
    cinturon_minimo = models.ForeignKey(
        Cinturon,
        on_delete=models.PROTECT,
        related_name='tecnicas',
        help_text='Cinturón a partir del cual se practica esta técnica',
    )

    class Meta:
        verbose_name = 'Técnica'
        ordering = ['categoria', 'nombre']

    def __str__(self):
        return f'{self.nombre} ({self.get_categoria_display()})'

