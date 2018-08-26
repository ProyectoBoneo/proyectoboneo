from rest_framework import serializers

from proyecto_boneo.apps.administracion.planes.models import Horario


class HorariosSerializer(serializers.ModelSerializer):
    materia = serializers.SerializerMethodField()

    def get_materia(self, obj):
        return obj.instancia_cursado.materia.descripcion

    class Meta:
        model = Horario
        fields = ['dia_semana', 'hora_inicio', 'hora_fin', 'materia']
