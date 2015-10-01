from django.db import models

from proyecto_boneo.apps.administracion.personal.models import Persona, PersonaLegajo
from proyecto_boneo.apps.administracion.planes.models import InstanciaCursado, Division
from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo


class Responsable(Persona):
    usuario = models.OneToOneField(UsuarioBoneo, related_name='responsable')


class Alumno(PersonaLegajo):
    usuario = models.OneToOneField(UsuarioBoneo, related_name='alumno')
    responsable = models.ForeignKey(Responsable, related_name='alumnos', on_delete=models.PROTECT)
    division = models.ForeignKey(Division)


class InscripcionAlumno(models.Model):
    alumno = models.ForeignKey(Alumno)
    instancia_cursado = models.ForeignKey(InstanciaCursado)
