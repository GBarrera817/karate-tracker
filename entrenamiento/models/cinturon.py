from django.db import models


class Cinturon(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    orden = models.PositiveIntegerField(unique=True, help_text="Posición en la progresión: 1=blanco, 2=amarillo, ...")
    color_hex = models.CharField(max_length=7, default="#FFFFFF", help_text="Color del cinturón, ej. #FFEB3B")
    sesiones_requeridas = models.PositiveIntegerField(default=0, help_text="Sesiones mínimas para optar a este cinturón")
    puede_crear_tecnicas = models.BooleanField(
        default=False,
        help_text='Si es True, quien tenga este cinturón puede crear técnicas (café y superiores)'
    )
    puede_promover = models.BooleanField(
        default=True,
        help_text='Si es True, quien tenga este cinturón puede promover a otros (negro y danes)'

    )

    class Meta:
        ordering = ["orden"]
        verbose_name = "Cinturón"
        verbose_name_plural = "Cinturones"

    def __str__(self):
        return self.nombre