from django.db import models

# Create your models here.
from proyecto_boneo.apps.administracion.alumnos.models import Alumno
from proyecto_boneo.apps.administracion.personal.models import Profesor
from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo


class Estadia(models.Model):
    usuario = models.ForeignKey(UsuarioBoneo)
    alumno = models.ForeignKey(Alumno)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return '{} - {}'.format(self.usuario, self.alumno)