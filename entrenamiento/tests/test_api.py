from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from entrenamiento.models import Cinturon, Practicante


class PromocionAPITests(APITestCase):
    """Prueba permisos, autenticación y códigos HTTP del endpoint de promociones."""

    def setUp(self):
        self.blanco = Cinturon.objects.create(nombre='Blanco', orden=1)
        self.amarillo = Cinturon.objects.create(nombre='Amarillo', orden=2)
        self.negro = Cinturon.objects.create(nombre='Negro', orden=7, puede_promover=True)

        # Sensei con autoridad
        self.u_sensei = User.objects.create_user('sensei', password='clave12345')
        self.sensei = Practicante.objects.create(user=self.u_sensei, rol=Practicante.SENSEI, cinturon_actual=self.negro)

        # Alumno raso, sin autoridad
        self.u_alumno = User.objects.create_user('alumno', password='clave12345')
        self.alumno = Practicante.objects.create(user=self.u_alumno, cinturon_actual=self.blanco)

    def autenticar(self, user):
        """Fuerza la autenticación del cliente como este user (sin pasar por /token/)."""

        self.client.force_authenticate(user=user)

    # ---- Autenticación ----------------------------------------------

    def test_sin_token_devuelve_401(self):
        """Un request sin autenticar es rechazado."""

        resp = self.client.get('/api/promociones/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # ---- Permisos ----------------------------------------------------

    def test_alumno_no_puede_promover_403(self):
        """Un alumno sin autoridad no puede crear promociones."""

        self.autenticar(self.u_alumno)
        resp = self.client.post('/api/promociones/', {
            'practicante': self.sensei.id,
            'cinturon_hasta': self.negro.id,
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_sensei_puede_promover_201(self):
        """Un sensei con autoridad promueve al grado siguiente correctamente."""
        self.autenticar(self.u_sensei)
        resp = self.client.post('/api/promociones/', {
            'practicante': self.alumno.id,
            'cinturon_hasta': self.amarillo.id,
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.alumno.refresh_from_db()
        self.assertEqual(self.alumno.cinturon_actual, self.amarillo)

    # ---- Reglas de negocios traducidad a HTTP ------------------------
    
    def test_salto_de_grado_devuelve_400(self):
        """El sensei tiene permiso, pero saltar grados es inválido: 400, no 403."""

        self.autenticar(self.u_sensei)
        resp = self.client.post('/api/promociones/', {
            'practicante': self.alumno.id,
            'cinturon_hasta': self.negro.id,  # de blanco a negro = salto
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_autopromocion_bloqueada(self):
        """Un sensei con autoridad no puede promoverse a sí mismo."""
        self.autenticar(self.u_sensei)
        resp = self.client.post('/api/promociones/', {
            'practicante': self.sensei.id,
            'cinturon_hasta': self.negro.id,
        })
        self.assertIn(resp.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    # ---- Endpoint de estadísticas -------------------------------------

    def test_estadisticas_accesibles_autenticado(self):

        self.autenticar(self.u_sensei)
        resp = self.client.get(f'/api/practicantes/{self.alumno.id}/estadisticas/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('porcentaje_asistencia', resp.data)

    def test_alumno_no_puede_crear_cinturon_403(self):
        self.autenticar(self.u_alumno)
        resp = self.client.post('/api/cinturones/', {'nombre': 'Verde', 'orden': 3})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_sensei_puede_crear_cinturon_201(self):
        self.autenticar(self.u_sensei)
        resp = self.client.post('/api/cinturones/', {'nombre': 'Verde', 'orden': 3})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_alumno_puede_leer_cinturones_200(self):
        """La lectura sigue abierta a cualquier autenticado."""
        self.autenticar(self.u_alumno)
        resp = self.client.get('/api/cinturones/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)