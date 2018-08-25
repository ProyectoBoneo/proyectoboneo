from rest_framework.serializers import ModelSerializer
from rest_framework import fields

from proyecto_boneo.apps.firebase.models import FireBaseToken
from proyecto_boneo.apps.api.usuarios.serializers import UsuarioBoneoSerializer


class FireBaseTokenSerializer(ModelSerializer):
    token = fields.CharField(max_length=255, required=True)
    user = UsuarioBoneoSerializer(required=False)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return FireBaseToken.objects.update_or_create(**validated_data)

    class Meta:
        fields = ['token', 'created_at', 'user']
        read_only_fields = ['created_at', 'updated_at', 'user']
        model = FireBaseToken
