from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo
from proyecto_boneo.apps.firebase.models import FireBaseToken


class Evento(models.Model):
    """
    Eventos organizados por la institución educativa
    Incluye una lista de participantes
    """
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    participantes = models.ManyToManyField(UsuarioBoneo, related_name='eventos')

    def __str__(self):
        if self.fecha_inicio != self.fecha_fin:
            return '{} ({} - {})'.format(self.nombre, self.fecha_inicio.strftime('%Y-%m-%d'),
                                         self.fecha_fin.strftime('%Y-%m-%d'))
        else:
            return '{} ({})'.format(self.nombre, self.fecha_inicio.strftime('%Y-%m-%d'))


@receiver(m2m_changed, sender=Evento.participantes.through)
def send_firebase_notifications(sender, instance=None, action=None, pk_set=None, **kwargs):
    if action == 'post_add':
        usuarios = UsuarioBoneo.objects.filter(pk__in=pk_set).all()
        for usuario in usuarios:
            FireBaseToken.send_notification(usuario, {
                'id': str(instance.id),
                'nombre': instance.nombre,
                'fecha_inicio': instance.fecha_inicio.isoformat(),
                'fecha_fin': instance.fecha_fin.isoformat()
            }, FireBaseToken.NOTIFICATION_TYPE_EVENTO)
