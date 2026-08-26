from django.db import models, transaction
from django.db.models import Count, Q
from django.core.exceptions import ValidationError
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

    # ------------------------------------------------------------------
    # Lógica de negocio
    # ------------------------------------------------------------------

    def siguiente_cinturon(self):
        """El cinturón inmediatamente superior al actual, o None si ya está en el máximo."""

        orden_actual = self.cinturon_actual.orden if self.cinturon_actual else 0

        return Cinturon.objects.filter(orden__gt=orden_actual).order_by('orden').first()

    @transaction.atomic
    def promover_a(self, cinturon_destino, otorgada_por):
        """
        Registra una promoción y actualiza el cinturón del practicante.
        Valida SOLO reglas estructurales; el criterio pedagógico es del sensei.
        Lanza ValidationError si la promoción es estructuralmente inválida.
        Devuelve la Promoción creada.
        """

        from .promocion import Promocion # import local: evita ciclo con promocion.py

        # Regla dura: nadie se promueve a si mismo (además del permiso de la API).
        
        if otorgada_por is not None and otorgada_por.id == self.id:
            raise ValidationError('Nadie puede promoverse a sí mismo.')

        siguiente = self.siguiente_cinturon()

        # Regla dura: ya está en el grado máximo.

        if siguiente is None:
            raise ValidationError('El practicante ya está en el cinturón más alto; no se puede promover.')

        # Regla dura: solo el siguiente grado. Ni saltos ni retroceso.

        if cinturon_destino.id != siguiente.id:
            raise ValidationError(
                f'Promoción inválida: desde "{self.cinturon_actual}" solo se puede promover a '
                f'"{siguiente}", no a "{cinturon_destino}".'
            )

        promocion = Promocion.objects.create(
            practicante=self,
            cinturon_desde=self.cinturon_actual,
            cinturon_hasta=cinturon_destino,
            otorgada_por=otorgada_por
        )

        self.cinturon_actual = cinturon_destino
        self.save(update_fields=['cinturon_actual'])

        return promocion

    def estadisticas_apoyo(self):
        """Datos informativos para que el sensei decida (NO bloquean la promocion)."""

        agg = self.sesiones.aggregate(
            total=Count('id'),
            presentes=Count('id', filter=Q(asistencia__presente=True)),
            ausentes=Count('id', filter=Q(asistencia__presente=False))
        )
        con_registro = agg['presentes'] + agg['ausentes']
        porcentaje = round(agg['presentes'] / con_registro * 100, 1) if con_registro else None
        siguiente = self.siguiente_cinturon()

        return {
            'sesiones_totales': agg['total'],
            'sesiones_presentes': agg['presentes'],
            'porcentaje_asistencia': porcentaje,
            'siguiente_cinturon': str(siguiente) if siguiente else None
        }
