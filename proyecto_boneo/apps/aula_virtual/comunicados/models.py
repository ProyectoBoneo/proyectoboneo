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
    comunicado = models.ForeignKey(Comunicado, on_delete=models.CASCADE)
    destinatario = models.ForeignKey(UsuarioBoneo, on_delete=models.CASCADE)
    fecha_leido = models.DateTimeField(null=True, blank=True)

    @property
    def leido(self):
        return self.fecha_leido is not None
