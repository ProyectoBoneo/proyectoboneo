from django.db import models
from django.db.models import Sum

from proyecto_boneo.apps.administracion.planes.models import Materia
from proyecto_boneo.apps.administracion.alumnos.models import Alumno


class ClaseVirtual(models.Model):
    EVALUACION = 'eva'
    EVALUACION_ESCRITA = 'esc'
    CLASE_NORMAL = 'nor'

    TIPO_CHOICES = (
        (CLASE_NORMAL, 'Clase Virtual'),
        (EVALUACION, 'Evaluación'),
        (EVALUACION_ESCRITA, 'Evaluación Escrita'),
    )

    materia = models.ForeignKey(Materia, related_name='clases_virtuales')
    nombre = models.CharField(max_length=30, default='Clase')
    descripcion = models.CharField(max_length=100)
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES)

    @property
    def descripcion_tipo(self):
        return [t[1] for t in self.TIPO_CHOICES if t[0] == self.tipo][0]

    def es_resuelta_alumno(self, alumno):
        return RespuestaEjercicioVirtual.objects.filter(clase_virtual=self).filter(alumno=alumno).count() > 0

    def es_corregida_alumno(self, alumno):
        respuesta_list = RespuestaEjercicioVirtual.objects.filter(clase_virtual=self)\
            .filter(alumno=alumno)
        for respuesta in respuesta_list:
            if respuesta.puntaje_obtenido == None:
                return False
        return True

    def obtener_puntaje_alumno(self, alumno):
        return RespuestaEjercicioVirtual.objects.filter(clase_virtual=self)\
            .filter(alumno=alumno).aggregate(Sum("puntaje_obtenido"))["puntaje_obtenido__sum"]

class EjercicioVirtual(models.Model):
    TEXTO = 'txt'
    MULTIPLE_CHOICE = 'mch'

    TIPO_CHOICES = (
        (TEXTO, 'Texto'),
        (MULTIPLE_CHOICE , 'Multiple Choice'),
    )

    tipo_ejercicio = models.CharField(max_length=3, choices=TIPO_CHOICES)
    clase_virtual = models.ForeignKey(ClaseVirtual, related_name='ejercicios')
    puntaje = models.FloatField(null=True, blank=True)
    orden_prioridad = models.IntegerField(null=True, blank=True)

    consigna = models.CharField(max_length=100)
    ayuda = models.TextField(null=True, blank=True)
    explicacion = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.consigna)

    @property
    def descripcion_tipo(self):
        return [t[1] for t in self.TIPO_CHOICES if t[0] == self.tipo][0]


class OpcionEjercicio(models.Model):
    texto = models.CharField(max_length=100)
    ejercicio = models.ForeignKey(EjercicioVirtual, related_name='opciones')
    opcion_correcta = models.BooleanField(default=False)


class RespuestaEjercicioVirtual(models.Model):
    alumno = models.ForeignKey(Alumno, related_name='respuestas')
    clase_virtual = models.ForeignKey(ClaseVirtual, related_name='respuestas')
    ejercicio = models.ForeignKey(EjercicioVirtual, related_name='respuestas')

    texto = models.TextField(null=True,default=None)
    opcion_seleccionada = models.ForeignKey(OpcionEjercicio, related_name='+', null=True)
    puntaje_obtenido = models.FloatField(null=True, blank=True)


class ResultadoEvaluacion(models.Model):
    clase_virtual = models.ForeignKey(ClaseVirtual, related_name='resultados')
    alumno = models.ForeignKey(Alumno, related_name='resultados_evaluaciones')
    nota = models.FloatField()
