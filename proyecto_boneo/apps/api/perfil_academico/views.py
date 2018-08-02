from rest_framework.views import APIView
from rest_framework.response import Response


class PerfilAcademicoAPIView(APIView):

    def get(self, request, *args, **kwargs):
        return Response({
            'result': 'ok'
        }, status=200)
