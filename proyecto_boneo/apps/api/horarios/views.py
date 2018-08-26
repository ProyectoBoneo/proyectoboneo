from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from proyecto_boneo.apps.api.horarios.serializers import HorariosSerializer


class HorariosViewSet(GenericViewSet, ListModelMixin):
    serializer_class = HorariosSerializer

    def get_queryset(self):
        horarios = []
        for inscripcion_alumno in self.request.user.alumno.inscripciones.all():
            horarios.extend(inscripcion_alumno.instancia_cursado.horarios.all())
        return sorted(horarios, key=lambda horario: '{}-{}'.format(horario.dia_semana, horario.hora_inicio))
