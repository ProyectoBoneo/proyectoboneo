from rest_framework.serializers import ModelSerializer, SerializerMethodField

from proyecto_boneo.apps.aula_virtual.clases.models import ClaseVirtual


class ClaseVirtualSerializer(ModelSerializer):
    tipo_y_materia = SerializerMethodField()

    def get_tipo_y_materia(self, obj):
        return '{} de {}'.format(obj.descripcion_tipo,  obj.materia.descripcion)

    class Meta:
        model = ClaseVirtual
        fields = ['nombre', 'descripcion', 'fecha', 'tipo_y_materia', 'id']
