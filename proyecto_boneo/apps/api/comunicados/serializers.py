from rest_framework import serializers

from proyecto_boneo.apps.aula_virtual.comunicados.models import Comunicado, DestinatarioComunicado


class ComunicadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comunicado
        fields = ['asunto', 'mensaje', 'fecha', 'emisor']


class DestinatarioComunicadosSerializer(serializers.ModelSerializer):
    comunicado = ComunicadosSerializer()

    class Meta:
        model = DestinatarioComunicado
        fields = ['comunicado', 'fecha_leido']
