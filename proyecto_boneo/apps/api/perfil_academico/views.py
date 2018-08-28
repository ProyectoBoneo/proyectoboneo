import datetime

from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response

from proyecto_boneo.apps.aula_virtual.clases.models import ResultadoEvaluacion
from proyecto_boneo.apps.api.perfil_academico.serializers import (PerfilAcademicoMateriasSerializer,
                                                                  ResultadoEvaluacionSerializer)


class PerfilAcademicoViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = PerfilAcademicoMateriasSerializer

    def get_queryset(self):
        return self.request.user.alumno.inscripciones.all()


class ResultadoEvaluacionViewSet(GenericViewSet):
    serializer_class = ResultadoEvaluacionSerializer

    @action(methods=['post'], detail=True)
    def mark_as_notified(self, request, pk):
        resultado_evaluacion = ResultadoEvaluacion.objects.get(pk=pk)
        resultado_evaluacion.fecha_notificado = datetime.datetime.now()
        resultado_evaluacion.save()
        return Response(self.serializer_class(resultado_evaluacion).data)
