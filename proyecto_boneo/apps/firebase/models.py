import logging

from requests.exceptions import HTTPError
from django.db import models
from firebase_admin import messaging

from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo

logger = logging.getLogger(__name__)


class FireBaseToken(models.Model):
    NOTIFICATION_TYPE_COMUNICADO = 'comunicado'
    NOTIFICATION_TYPES = [
        NOTIFICATION_TYPE_COMUNICADO
    ]
    token = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(UsuarioBoneo, related_name='firebase_tokens', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def send_notification(cls, user, data, notification_type):
        for firebase_token in user.firebase_tokens.all():
            message = messaging.Message(
                data={**data, 'notification_type': notification_type},
                token=firebase_token.token
            )
            try:
                messaging.send(message)
            except HTTPError as e:
                logger.error('There was an error while sending firebase notification', e)
