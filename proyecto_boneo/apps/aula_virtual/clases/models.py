from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from proyecto_boneo.apps.administracion.planes.models import Materia
from proyecto_boneo.apps.administracion.alumnos.models import Alumno, InscripcionAlumno
from proyecto_boneo.apps.administracion.planes.models import InstanciaCursado
from proyecto_boneo.apps.firebase.models import FireBaseToken


class ClaseVirtual(models.Model):

    class Meta:
        ordering = ('tipo', 'descripcion')

    EVALUACION = 'eva'
    EVALUACION_ESCRITA = 'esc'
    CLASE_NORMAL = 'nor'

    TIPO_CHOICES = (
        (CLASE_NORMAL, 'Clase Virtual'),
        (EVALUACION, 'Evaluación'),
        (EVALUACION_ESCRITA, 'Evaluación Escrita'),
    )
    fecha = models.DateField(auto_now_add=True)
    materia = models.ForeignKey(Materia, related_name='clases_virtuales', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30, default='Clase')
    descripcion = models.CharField(max_length=100)
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES)
    publicado = models.BooleanField(null=False, default=True)

    @property
    def descripcion_tipo(self):
        return [t[1] for t in self.TIPO_CHOICES if t[0] == self.tipo][0]

    def es_resuelta_alumno(self, alumno):
        return RespuestaEjercicioVirtual.objects.filter(clase_virtual=self).filter(alumno=alumno).count() > 0

    def es_corregida_alumno(self, alumno):
        respuesta_list = RespuestaEjercicioVirtual.objects.filter(clase_virtual=self).filter(alumno=alumno)
        for respuesta in respuesta_list:
            if respuesta.puntaje_obtenido is None:
                return False
        return True

    def obtener_puntaje_alumno(self, alumno):
        return RespuestaEjercicioVirtual.objects.filter(clase_virtual=self).filter(
            alumno=alumno).aggregate(Sum("puntaje_obtenido"))["puntaje_obtenido__sum"]


class EjercicioVirtual(models.Model):
    TEXTO = 'txt'
    MULTIPLE_CHOICE = 'mch'

    TIPO_CHOICES = (
        (TEXTO, 'Texto'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),
    )

    tipo_ejercicio = models.CharField(max_length=3, choices=TIPO_CHOICES)
    clase_virtual = models.ForeignKey(ClaseVirtual, related_name='ejercicios', on_delete=models.CASCADE)
    puntaje = models.FloatField(null=True, blank=True)
    orden_prioridad = models.IntegerField(null=True, blank=True)

    consigna = models.CharField(max_length=100)
    ayuda = models.TextField(null=True, blank=True)
    explicacion = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.consigna)

    @property
    def descripcion_tipo(self):
        return [t[1] for t in self.TIPO_CHOICES if t[0] == self.tipo_ejercicio][0]


class OpcionEjercicio(models.Model):
    texto = models.CharField(max_length=100)
    ejercicio = models.ForeignKey(EjercicioVirtual, related_name='opciones', on_delete=models.CASCADE)
    opcion_correcta = models.BooleanField(default=False)


class RespuestaEjercicioVirtual(models.Model):
    alumno = models.ForeignKey(Alumno, related_name='respuestas', on_delete=models.CASCADE)
    clase_virtual = models.ForeignKey(ClaseVirtual, related_name='respuestas', on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(EjercicioVirtual, related_name='respuestas', on_delete=models.CASCADE)

    texto = models.TextField(null=True, default=None)
    opcion_seleccionada = models.ForeignKey(OpcionEjercicio, related_name='+', null=True, on_delete=models.CASCADE)
    puntaje_obtenido = models.FloatField(null=True, blank=True)
    observaciones = models.TextField(null=True, default=None, blank=True)


class ResultadoEvaluacion(models.Model):
    clase_virtual = models.ForeignKey(ClaseVirtual, related_name='resultados', on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, related_name='resultados_evaluaciones', on_delete=models.CASCADE)
    nota = models.FloatField()
    fecha_correccion = models.DateTimeField(auto_now=True)
    fecha_notificado = models.DateTimeField(null=True, default=None)


@receiver(post_save, sender=ResultadoEvaluacion)
def send_resultado_evaluacion_firebase_notifications(sender, instance=None, created=False, **kwargs):
    if created:
        inscripcion_alumno = InscripcionAlumno.objects.filter(
            alumno=instance.alumno, instancia_cursado__materia=instance.clase_virtual.materia).first()
        FireBaseToken.send_notification(instance.alumno.usuario, {
            'id': str(instance.id),
            'inscripcion_alumno_id': str(inscripcion_alumno.id),
            'fecha': instance.clase_virtual.fecha.isoformat(),
            'evaluacion': instance.clase_virtual.nombre,
        }, FireBaseToken.NOTIFICATION_TYPE_PERFIL_ACADEMICO)


@receiver(post_save, sender=ClaseVirtual)
def send_clase_virtual_firebase_notifications(sender, instance=None, created=False, **kwargs):
    if created:
        alumnos = Alumno.objects.filter(inscripciones__instancia_cursado__in=InstanciaCursado.objects.año_actual(),
                                        inscripciones__instancia_cursado__materia=instance.materia).distinct()
        for alumno in alumnos:
            FireBaseToken.send_notification(alumno.usuario, {
                'id': str(instance.id),
                'fecha': instance.fecha.isoformat(),
                'nombre': instance.nombre,
                'materia': str(instance.materia),
            }, FireBaseToken.NOTIFICATION_TYPE_CLASE_VIRTUAL)
