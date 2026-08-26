from rest_framework.routers import DefaultRouter
from .views import (
    CinturonViewSet,
    TecnicaViewSet,
    PracticanteViewSet,
    SesionViewSet,
    AsistenciaViewSet,
    PromocionViewSet,
)


router = DefaultRouter()
router.register(r'cinturones', CinturonViewSet)
router.register(r"tecnicas", TecnicaViewSet)
router.register(r"practicantes", PracticanteViewSet)
router.register(r"sesiones", SesionViewSet, basename='sesion')
router.register(r"asistencias", AsistenciaViewSet)
router.register(r"promociones", PromocionViewSet)

urlpatterns = router.urls
