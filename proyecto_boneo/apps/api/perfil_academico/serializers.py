from rest_framework import serializers

from proyecto_boneo.apps.administracion.alumnos.models import InscripcionAlumno
from proyecto_boneo.apps.aula_virtual.clases.models import ClaseVirtual, ResultadoEvaluacion


class PerfilAcademicoMateriasSerializer(serializers.ModelSerializer):
    anio_cursado = serializers.SerializerMethodField()
    nombre_materia = serializers.SerializerMethodField()
    division = serializers.SerializerMethodField()
    evaluaciones = serializers.SerializerMethodField()

    def get_anio_cursado(self, obj):
        return obj.instancia_cursado.anio_cursado

    def get_nombre_materia(self, obj):
        return obj.instancia_cursado.materia.descripcion

    def get_division(self, obj):
        return str(obj.instancia_cursado.division)

    def get_evaluaciones(self, obj):
        resultados_evaluaciones = ResultadoEvaluacion.objects.filter(
            alumno=obj.alumno, clase_virtual__materia=obj.instancia_cursado.materia,
            clase_virtual__tipo__in=[ClaseVirtual.EVALUACION, ClaseVirtual.EVALUACION_ESCRITA]
        ).all()
        return [
            {
                'id': resultado_evaluacion.id,
                'nota': resultado_evaluacion.nota,
                'evaluacion': resultado_evaluacion.clase_virtual.nombre,
                'descricpion': resultado_evaluacion.clase_virtual.descripcion,
                'fecha_notificado': resultado_evaluacion.fecha_notificado,
                'fecha_correccion': resultado_evaluacion.fecha_correccion,

            } for resultado_evaluacion in resultados_evaluaciones
        ]

    class Meta:
        model = InscripcionAlumno
        fields = ['promedio', 'anio_cursado', 'nombre_materia', 'division', 'evaluaciones']
