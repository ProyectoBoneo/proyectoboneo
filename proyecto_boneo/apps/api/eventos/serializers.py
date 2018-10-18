from rest_framework.serializers import ModelSerializer

from proyecto_boneo.apps.administracion.eventos.models import Evento


class EventoSerializer(ModelSerializer):
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'id']

