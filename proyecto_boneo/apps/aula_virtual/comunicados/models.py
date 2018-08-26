import logging

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from firebase_admin import messaging
from requests.exceptions import HTTPError

from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo


logger = logging.getLogger(__name__)


class Comunicado(models.Model):
    asunto = models.CharField(max_length=150)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_leido = models.DateTimeField(null=True, blank=True)
    emisor = models.ForeignKey(UsuarioBoneo, on_delete=models.PROTECT, related_name="usuario_emisor")
    destinatarios = models.ManyToManyField(UsuarioBoneo, through='DestinatarioComunicado')

    def __str__(self):
        return self.asunto


class DestinatarioComunicado(models.Model):
    comunicado = models.ForeignKey(Comunicado, on_delete=models.CASCADE)
    destinatario = models.ForeignKey(UsuarioBoneo, on_delete=models.CASCADE)
    fecha_leido = models.DateTimeField(null=True, blank=True)

    @property
    def leido(self):
        return self.fecha_leido is not None


@receiver(post_save, sender=DestinatarioComunicado)
def send_firebase_notifications(sender, instance=None, created=False, **kwargs):
    if created:
        for firebase_token in instance.destinatario.firebase_tokens.all():
            message = messaging.Message(
                data={
                    'destinatario_comunicado': str(instance.id),
                    'emisor': instance.comunicado.emisor.username,
                    'fecha': instance.comunicado.fecha.isoformat()
                },
                notification=messaging.Notification(
                    title='Nuevo comunicado',
                    body=instance.comunicado.emisor.username,
                ),
                token=firebase_token.token
            )
            try:
                messaging.send(message)
            except HTTPError as e:
                logger.error('There was an error while sending firebase notification', e)
