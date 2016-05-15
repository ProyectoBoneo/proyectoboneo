from django.db import models

from proyecto_boneo.apps.administracion.personal.models import Persona, PersonaLegajo
from proyecto_boneo.apps.administracion.planes.models import InstanciaCursado, Division, ClaseReal
from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo


class Responsable(Persona):
    usuario = models.OneToOneField(UsuarioBoneo, related_name='responsable')


class Alumno(PersonaLegajo):
    usuario = models.OneToOneField(UsuarioBoneo, related_name='alumno')
    responsable = models.ForeignKey(Responsable, related_name='alumnos', on_delete=models.PROTECT)
    division = models.ForeignKey(Division, related_name='alumnos', null=True, blank=True)

    def crear_usuario(self, email):
        super(Alumno, self).crear_usuario(email)
        self.usuario.is_alumno = True
        self.usuario.save()


class InscripcionAlumno(models.Model):
    alumno = models.ForeignKey(Alumno, related_name='inscripciones')
    instancia_cursado = models.ForeignKey(InstanciaCursado, related_name='inscripciones')


class Asistencia(models.Model):
        fecha = models.DateField()
        alumno = models.ForeignKey(Alumno, related_name='asistencias')
        division = models.ForeignKey(Division, related_name='asistentes')
        # clase_real = models.ForeignKey(ClaseReal, related_name='asistentes')
        asistio = models.BooleanField(default=False)