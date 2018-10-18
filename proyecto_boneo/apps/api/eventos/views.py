import datetime

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from proyecto_boneo.apps.administracion.eventos.models import Evento


from proyecto_boneo.apps.api.eventos.serializers import EventoSerializer


class EventosViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = EventoSerializer

    def get_queryset(self):
        return Evento.objects.filter(participantes__in=[self.request.user],
                                     fecha_fin__gte=datetime.date.today()).order_by('fecha_inicio')
