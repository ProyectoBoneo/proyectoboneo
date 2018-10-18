import datetime

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from proyecto_boneo.apps.aula_virtual.clases.models import ClaseVirtual

from proyecto_boneo.apps.api.clases_virtuales.serializers import ClaseVirtualSerializer


class ClasesVirtualesViewSet(GenericViewSet, ListModelMixin):
    serializer_class = ClaseVirtualSerializer

    def get_queryset(self):
        return ClaseVirtual.objects.filter(
            materia__instancias_cursado__inscripciones__alumno=self.request.user.alumno,
            fecha__gte=datetime.date.today(),
            publicado=True).distinct()
