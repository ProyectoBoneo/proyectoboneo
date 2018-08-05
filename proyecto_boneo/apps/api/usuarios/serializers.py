from rest_framework.serializers import ModelSerializer

from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo


class UsuarioBoneoSerializer(ModelSerializer):

    class Meta:
        model = UsuarioBoneo
        fields = ['username', 'is_alumno', 'is_profesor', 'is_staff', 'first_name', 'last_name']
