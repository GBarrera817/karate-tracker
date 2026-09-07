from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from entrenamiento.models import Cinturon, Practicante


class PromocionModelTests(TestCase):

    """Prueba la lógica de negociio de Practicvante.promover_a directamente."""

    def setUp(self):
        # Catalogo de cinturones (orden con huecos a propósito: 1, 2, 7)
        # para verificar que 'siguiente' usa orden__gt y no orden+1.
         
        self.blanco = Cinturon.objects.create(nombre='Blanco', orden=1)
        self.amarillo = Cinturon.objects.create(nombre='Amarillo', orden=2)
        self.negro = Cinturon.objects.create(nombre='Negro', orden=7, puede_promover=True) 

        self.sensei = Practicante.objects.create(
            user=User.objects.create_user('sensei'),
            rol=Practicante.SENSEI,
            cinturon_actual=self.negro
        )
        self.alumno = Practicante.objects.create(
            user=User.objects.create_user('alumno'),
            cinturon_actual=self.blanco
        )

    # ----------- CASOS QUE DEBEN FUNCIONAR -----------------------------------
    
    def test_promocion_valida_actualiza_cinturon(self):
        """Promover al grado inmediato superior actualiza cinturon_actual."""

        promo = self.alumno.promover_a(self.amarillo, otorgada_por=self.sensei)
        self.alumno.refresh_from_db()
        self.assertEqual(self.alumno.cinturon_actual, self.amarillo)

        # Y deja registro histórico correcto
        self.assertEqual(promo.cinturon_desde, self.blanco)
        self.assertEqual(promo.cinturon_hasta, self.amarillo)
        self.assertEqual(promo.otorgada_por, self.sensei)

    def test_siguiente_cinturon_salta_huecos_de_orden(self):
        """ Desde amarillo (orden 2), el siguiente es negro (orden 7), no orden 3."""
        self.alumno.cinturon_actual = self.amarillo
        self.alumno.save()
        self.assertEqual(self.alumno.siguiente_cinturon(), self.negro)

    # ----------- Casos que deben FALLAR (las reglas duras) -------------------

    def test_no_permite_saltar_grados(self):
        """De blanco no se puede ir directo a negro."""

        with self.assertRaises(ValidationError):
            self.alumno.promover_a(self.negro, otorgada_por=self.sensei)

        # Y el cinturón NO cambió
        self.alumno.refresh_from_db()
        self.assertEqual(self.alumno.cinturon_actual, self.blanco)

    def test_no_permite_retroceder(self):
        """Un practicante en amarillo no puede 'promover' a blanco."""
        self.alumno.cinturon_actual = self.amarillo
        self.alumno.save()

        with self.assertRaises(ValidationError):
            self.alumno.promover_a(self.blanco, otorgada_por=self.sensei)

    def test_no_se_puede_autopromover(self):
        """Aunque tenga autoridad, nadie se promueve a sí mismo."""

        with self.assertRaises(ValidationError):
            self.sensei.promover_a(self.negro, otorgada_por=self.sensei)

    def test_no_promueve_desde_el_grado_maximo(self):
        """Quien ya está en el cinturón más alto no tiiene a donde subir."""

        # sensei está en negro (el máximo). No hay siguiente.
        self.assertIsNone(self.sensei.siguiente_cinturon())

    # ----- Atomicidad ----------------------------------------------

    def test_fallo_no_deja_datos_a_medias(self):
        """Si la promoción es inválida, no se crea ningún registro histórico."""

        from entrenamiento.models import Promocion

        conteo_antes = Promocion.objects.count()

        with self.assertRaises(ValidationError):
            self.alumno.promover_a(self.negro, otorgada_por=self.sensei) # salto inválido

        self.assertEqual(Promocion.objects.count(), conteo_antes)