from rest_framework.views import APIView
from rest_framework.response import Response

from proyecto_boneo.apps.administracion.eventos.models import Evento
from proyecto_boneo.apps.aula_virtual.clases.models import ClaseVirtual

from proyecto_boneo.apps.api.eventos.serializers import ClaseVirtualSerializer, EventoSerializer


class EventosView(APIView):
    def get(self, request, *args, **kwargs):
        eventos = Evento.objects.filter(participantes__in=[request.user])
        clases = ClaseVirtual.objects.filter(
            materia__instancias_cursado__inscripciones__alumno=self.request.user.alumno, publicado=True).distinct()
        return Response({
            'eventos': EventoSerializer(eventos, many=True).data,
            'clases': ClaseVirtualSerializer(clases, many=True).data,
        })
