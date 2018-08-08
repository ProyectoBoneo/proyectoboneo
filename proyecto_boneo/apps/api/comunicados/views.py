import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from proyecto_boneo.apps.aula_virtual.comunicados.models import DestinatarioComunicado
from proyecto_boneo.apps.api.comunicados.serializers import DestinatarioComunicadosSerializer


class ComunicadosViewSet(viewsets.ModelViewSet):
    serializer_class = DestinatarioComunicadosSerializer

    @action(methods=['post'], detail=True)
    def mark_as_read(self, request, pk):
        destinatario_comunicado = DestinatarioComunicado.objects.get(pk=pk)
        destinatario_comunicado.fecha_leido = datetime.datetime.now()
        destinatario_comunicado.save()
        return Response(self.serializer_class(destinatario_comunicado).data)

    def get_queryset(self):
        return DestinatarioComunicado.objects.filter(destinatario=self.request.user)
