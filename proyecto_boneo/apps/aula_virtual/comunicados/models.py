from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo
from proyecto_boneo.apps.firebase.models import FireBaseToken


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
        FireBaseToken.send_notification(instance.destinatario, {
            'id': str(instance.id),
            'emisor': instance.comunicado.emisor.username,
            'fecha': instance.comunicado.fecha.isoformat()
        }, FireBaseToken.NOTIFICATION_TYPE_COMUNICADO)
