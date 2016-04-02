from django.db import models

from proyecto_boneo.apps.administracion.planes.models import Materia
from proyecto_boneo.apps.administracion.alumnos.models import Alumno


class ClaseVirtual(models.Model):
    #  TODO: Agregar criterios de evaluación y puntaje por ejercicio
    # TODO: Pertenece a un profesor quien la administra o puede ser editada por cualquier profesor
    materia = models.ForeignKey(Materia, related_name='clases_virtuales')
    nombre = models.CharField(max_length=30, default="Clase")
    descripcion = models.CharField(max_length=100)

class EjercicioVirtual(models.Model):
    titulo = models.CharField(max_length=30)
    clase_virtual = models.ForeignKey(ClaseVirtual, related_name='ejercicios')

    def __str__(self):
        return '{}'.format(self.titulo)

class EjercicioVirtualTexto(EjercicioVirtual):
    ayuda = models.TextField(null=True, blank=True)
    consigna = models.CharField(max_length=100)
    orden_prioridad = models.IntegerField(null=True, blank=True)


class EjercicioVirtualMultipleChoice(EjercicioVirtual):
    ayuda = models.TextField(null=True, blank=True)
    pregunta = models.CharField(max_length=100)
    explicacion = models.TextField(null=True, blank=True)
    orden_prioridad = models.IntegerField(null=True, blank=True)


class OpcionEjercicioMultipleChoice(models.Model):
    texto = models.CharField(max_length=100)
    ejercicio = models.ForeignKey(EjercicioVirtualMultipleChoice, related_name='opciones')
    opcion_correcta = models.BooleanField(default=False)


class RespuestaEjercicioVirtual(models.Model):
    alumno = models.ForeignKey(Alumno, related_name='+')


class RespuestaEjercicioVirtualTexto(RespuestaEjercicioVirtual):
    texto = models.TextField()
    ejercicio = models.ForeignKey(EjercicioVirtualTexto, related_name='respuestas')


class RespuestaEjercicioVirtualMultipleChoice(RespuestaEjercicioVirtual):
    opcion_seleccionada = models.ForeignKey(OpcionEjercicioMultipleChoice, related_name='+')
    ejercicio = models.ForeignKey(EjercicioVirtualMultipleChoice, related_name='respuestas')
