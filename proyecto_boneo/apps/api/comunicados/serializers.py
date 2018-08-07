from rest_framework import serializers

from proyecto_boneo.apps.aula_virtual.comunicados.models import Comunicado, DestinatarioComunicado
from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo


class EmisorSerializer(serializers.ModelSerializer):
    nombre = serializers.SerializerMethodField()

    def _get_persona_model(self, obj):
        if obj.is_alumno:
            return obj.alumno
        elif obj.is_profesor:
            return obj.profesor
        elif obj.is_staff:
            return obj
        else:
            return obj.responsable

    def get_nombre(self, obj):
        return self._get_persona_model(obj).descripcion

    class Meta:
        model = UsuarioBoneo
        fields = ['username', 'nombre']


class ComunicadosSerializer(serializers.ModelSerializer):
    emisor = EmisorSerializer()

    class Meta:
        model = Comunicado
        fields = ['asunto', 'mensaje', 'fecha', 'emisor', 'id']


class DestinatarioComunicadosSerializer(serializers.ModelSerializer):
    comunicado = ComunicadosSerializer()

    class Meta:
        model = DestinatarioComunicado
        fields = ['comunicado', 'fecha_leido', 'id']
