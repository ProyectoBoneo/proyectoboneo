from rest_framework import serializers

from proyecto_boneo.apps.administracion.alumnos.models import Alumno, InscripcionAlumno
from proyecto_boneo.apps.administracion.planes.models import InstanciaCursado
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


class InstanciaCursadoSerializer(serializers.ModelSerializer):
    emisor = EmisorSerializer()

    class Meta:
        model = InstanciaCursado
        fields = ['anio_cursado', 'nombre_materia', 'division']


class InscripcionesSerializer(serializers.ModelSerializer):
    anio_cursado = serializers.SerializerMethodField()
    nombre_materia = serializers.SerializerMethodField()
    division = serializers.SerializerMethodField()

    def get_anio_cursado(self, obj):
        return obj.instancia_cursado.anio_cursado

    def get_nombre_materia(self, obj):
        return obj.instancia_cursado.materia.descripcion

    def get_division(self, obj):
        return str(obj.instancia_cursado.division)

    class Meta:
        model = InscripcionAlumno
        fields = ['promedio', 'anio_cursado', 'nombre_materia', 'division']
