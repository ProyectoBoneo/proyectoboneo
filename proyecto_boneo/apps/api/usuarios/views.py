from rest_framework.views import APIView
from rest_framework.response import Response

from proyecto_boneo.apps.api.usuarios.serializers import UsuarioBoneoSerializer


class UsuarioBoneoView(APIView):

    def get(self, request, *args, **kwargs):
        return Response(UsuarioBoneoSerializer(request.user).data)
