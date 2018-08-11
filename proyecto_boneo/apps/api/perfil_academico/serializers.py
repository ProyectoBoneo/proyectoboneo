from rest_framework import serializers

from proyecto_boneo.apps.administracion.alumnos.models import InscripcionAlumno
from proyecto_boneo.apps.aula_virtual.clases.models import ClaseVirtual, ResultadoEvaluacion


class ResultadoEvaluacionSerializer(serializers.ModelSerializer):
    evaluacion = serializers.SerializerMethodField()
    descripcion = serializers.SerializerMethodField()

    def get_evaluacion(self, obj):
        return obj.clase_virtual.nombre

    def get_descripcion(self, obj):
        return obj.clase_virtual.descripcion

    class Meta:
        model = ResultadoEvaluacion
        fields = ['id', 'nota', 'evaluacion', 'descripcion', 'fecha_notificado', 'fecha_correccion']


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
        return ResultadoEvaluacionSerializer(resultados_evaluaciones, many=True).data

    class Meta:
        model = InscripcionAlumno
        fields = ['promedio', 'anio_cursado', 'nombre_materia', 'division', 'evaluaciones']
