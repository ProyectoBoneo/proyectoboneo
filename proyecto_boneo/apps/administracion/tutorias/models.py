from django.db import models

# Create your models here.
from proyecto_boneo.apps.administracion.alumnos.models import Alumno
from proyecto_boneo.apps.administracion.personal.models import Profesor



class Tutoria(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    anio = models.IntegerField()

    def __str__(self):
        return '{} - {} - {}'.format(self.anio, self.profesor, self.alumno)

class EncuentroTutoria(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    tutoria = models.ForeignKey(Tutoria, on_delete=models.CASCADE)
    resumen = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.fecha)

    class Meta:
        ordering = ['fecha']