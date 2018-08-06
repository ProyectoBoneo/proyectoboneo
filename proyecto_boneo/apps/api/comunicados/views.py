from rest_framework import viewsets

from proyecto_boneo.apps.aula_virtual.comunicados.models import DestinatarioComunicado
from proyecto_boneo.apps.api.comunicados.serializers import DestinatarioComunicadosSerializer


class ComunicadosViewSet(viewsets.ModelViewSet):
    serializer_class = DestinatarioComunicadosSerializer

    def get_queryset(self):
        return DestinatarioComunicado.objects.filter(destinatario=self.request.user)
