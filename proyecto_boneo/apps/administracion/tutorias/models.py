from django.db import models

# Create your models here.
from proyecto_boneo.apps.administracion.alumnos.models import Alumno
from proyecto_boneo.apps.administracion.personal.models import Profesor


class Tutoria(models.Model):
    profesor = models.ForeignKey(Profesor)
    alumno = models.ForeignKey(Alumno)
    anio = models.IntegerField()

    def __str__(self):
        return '{} - {} - {}'.format(self.anio, self.profesor, self.alumno)

class EncuentroTutoria(models.Model):
    fecha = models.DateTimeField()
    tutoria = models.ForeignKey(Tutoria)
    resumen = models.TextField(null=True, blank=True)
    # TODO: observacionesProfesor (privada para el)
    # TODO:Agregar lugar punto de encuentro
    # TODO: retroalimentacionAlumno (el alumno puede ingresar solo este dato) nullable

    def __str__(self):
        return '{}'.format(self.fecha.date())

    class Meta:
        ordering = ['fecha']