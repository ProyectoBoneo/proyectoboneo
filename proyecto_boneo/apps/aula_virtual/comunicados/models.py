from django.db import models
from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo


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
    comunicado = models.ForeignKey(Comunicado)
    destinatario = models.ForeignKey(UsuarioBoneo)
    fecha_leido = models.DateTimeField(null=True, blank=True)
