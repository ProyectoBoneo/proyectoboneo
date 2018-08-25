from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from proyecto_boneo.apps.firebase.models import FireBaseToken
from proyecto_boneo.apps.api.firebase.serializers import FireBaseTokenSerializer


class FireBaseTokenViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = FireBaseTokenSerializer

    def get_queryset(self):
        return FireBaseToken.objects.filter(user=self.request.user).all()
