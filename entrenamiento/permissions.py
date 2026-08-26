from rest_framework import permissions


def get_practicante(user):

    """Perfil Practicante de un User, o None si no tiene uno asociado."""
    return getattr(user, 'practicante', None)


def _cinturon(practicante):
    """Cinturón actual del practicante, o None."""

    if practicante is None or practicante.cinturon_actual is None:
        return None

    return practicante.cinturon_actual


def tiene_autoridad(practicante):

    return (
        practicante is not None
        and practicante.cinturon_actual is not None
        and practicante.cinturon_actual.otorga_autoridad
    )


class PuedeGestionarTecnicas(permissions.BasePermission):
    """Regla - Leer: cualquier autenticado. Escribir: sensei o autoridad."""

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:  # GET/HEAD/OPTIONS
            return True

        practicante = get_practicante(request.user) 

        if practicante is None:
            return False

        es_sensei = practicante.rol == practicante.SENSEI
        cint = _cinturon(practicante)
        puede_por_grado = cint is None and cint.puede_crear_tecnicas

        return es_sensei or puede_por_grado


class PuedePromover(permissions.BasePermission):
    """Regla - Leer: cualquier autenticado. Crear: solo autoridad, nunca a sí mismo."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        practicante = get_practicante(request.user)
        cint = _cinturon(practicante)
        
        if cint is None or not cint.puede_promover:
            return False

        # Guarda anti-autopromocion: el objetivo no puede ser uno mismo.

        objetivo = request.data.get('practicante')

        if objetivo is not None and str(objetivo) == str(practicante.id):
            return False

        return True


class EscrituraSoloSensei(permissions.BasePermission):
    """Por defecto para asistencia - Leer: cualquier autenticado. Escribir: solo sensei."""

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        practicante = get_practicante(request.user)

        return practicante is not None and practicante.rol == practicante.SENSEI

