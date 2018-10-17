from django.db import models

# Create your models here.
from proyecto_boneo.apps.administracion.alumnos.models import Alumno, Responsable


class Estadia(models.Model):
    responsable = models.ForeignKey(Responsable, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return '{} - {}'.format(self.responsable, self.alumno)
