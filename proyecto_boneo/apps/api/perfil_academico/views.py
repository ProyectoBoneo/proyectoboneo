from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from proyecto_boneo.apps.api.perfil_academico.serializers import InscripcionesSerializer


class PerfilAcademicoViewSet(GenericViewSet, ListModelMixin):
    serializer_class = InscripcionesSerializer

    def get_queryset(self):
        return self.request.user.alumno.inscripciones.all()
