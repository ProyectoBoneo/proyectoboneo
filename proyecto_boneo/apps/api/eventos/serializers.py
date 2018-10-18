from rest_framework.serializers import ModelSerializer, SerializerMethodField

from proyecto_boneo.apps.administracion.eventos.models import Evento
from proyecto_boneo.apps.aula_virtual.clases.models import ClaseVirtual


class EventoSerializer(ModelSerializer):
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'id']


class ClaseVirtualSerializer(ModelSerializer):
    materia = SerializerMethodField()

    def get_materia(self, obj):
        return obj.materia.descripcion

    class Meta:
        model = ClaseVirtual
        fields = ['nombre', 'descripcion', 'tipo', 'fecha', 'materia', 'id']
