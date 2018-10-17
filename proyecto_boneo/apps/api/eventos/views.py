from rest_framework.views import APIView

from proyecto_boneo.apps.administracion.eventos.models import Evento
from proyecto_boneo.apps.aula_virtual.clases.models import ClaseVirtual


class EventosView(APIView):

    def get(self, request, *args, **kwargs):
        pass
