from django.db import models

from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo


class FireBaseToken(models.Model):
    token = models.CharField(max_length=255, primary_key=True)
    user = models.OneToOneField(UsuarioBoneo, related_name='firebase_token',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
