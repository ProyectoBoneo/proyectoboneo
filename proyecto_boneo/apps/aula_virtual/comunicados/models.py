from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo
from proyecto_boneo.apps.administracion.planes.models import Division
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
    TYPE_USER = 'usuario'
    TYPE_DIVISION = 'division'
    TYPE_YEAR = 'anio'
    TYPE_USER_GROUP = 'user_group'

    USER_GROUP_ALUMNOS = 'alumnos'
    USER_GROUP_PROFESORES = 'profesores'
    USER_GROUP_ADMIN = 'admin'

    USER_GROUPS = [
        ('Alumnos', USER_GROUP_ALUMNOS),
        ('Profesores', USER_GROUP_PROFESORES),
        ('Administración', USER_GROUP_ADMIN),
    ]

    comunicado = models.ForeignKey(Comunicado, on_delete=models.CASCADE)
    destinatario = models.ForeignKey(UsuarioBoneo, on_delete=models.CASCADE)
    fecha_leido = models.DateTimeField(null=True, blank=True)

    @property
    def leido(self):
        return self.fecha_leido is not None

    @classmethod
    def build_destinatario_id(cls, destinatario_type, destinatario_id):
        return '{}_{}'.format(destinatario_type, destinatario_id)

    @classmethod
    def get_possible_destinatarios(cls):
        possible_destinatarios = []
        possible_destinatarios.extend({'id': cls.build_destinatario_id(cls.TYPE_USER, user.id),
                                       'text': user.get_full_name(),
                                       'subtext': user.username}
                                      for user in UsuarioBoneo.objects.all())
        possible_destinatarios.extend({'id': cls.build_destinatario_id(cls.TYPE_DIVISION, division.id),
                                       'text': str(division),
                                       'subtext': 'División'}
                                      for division in Division.objects.filter(activa=True).all())
        possible_destinatarios.extend({'id': cls.build_destinatario_id(cls.TYPE_YEAR, anio),
                                       'text': '{}º'.format(anio),
                                       'subtext': 'Año de cursado'}
                                      for anio in Division.objects.años_plan())
        possible_destinatarios.extend({
            'id': cls.build_destinatario_id(cls.TYPE_USER_GROUP, group[1]),
            'text': group[0],
            'subtext': 'Grupo de usuarios'
        } for group in cls.USER_GROUPS)
        return possible_destinatarios


@receiver(post_save, sender=DestinatarioComunicado)
def send_firebase_notifications(sender, instance=None, created=False, **kwargs):
    if created:
        FireBaseToken.send_notification(instance.destinatario, {
            'id': str(instance.id),
            'emisor': instance.comunicado.emisor.username,
            'fecha': instance.comunicado.fecha.isoformat()
        }, FireBaseToken.NOTIFICATION_TYPE_COMUNICADO)
