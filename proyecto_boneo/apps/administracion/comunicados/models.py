import re

from django.core.validators import RegexValidator
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from proyecto_boneo.apps.administracion.planes.models import InstanciaCursado
from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo


class Comunicado(models.Model):
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    emisor = models.ForeignKey(UsuarioBoneo, on_delete=models.PROTECT, related_name="usuario_emisor")
    destinatarios = models.ManyToManyField(UsuarioBoneo)
    # TODO:Ver si dejamos esto como historico.
    # grupo_receptor = models.ForeignKey(Grupo, null=True, blank=True)
    # instancia_cursado_receptor = models.ForeignKey(InstanciaCursado, null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.fecha.date(), self.mensaje[:15] + "...")

# class Destinatario(models.Model):
#     comunicado = models.ForeignKey(Comunicado, on_delete=models.PROTECT)
#     destinatario = models.ForeignKey(UsuarioBoneo, on_delete=models.PROTECT)

