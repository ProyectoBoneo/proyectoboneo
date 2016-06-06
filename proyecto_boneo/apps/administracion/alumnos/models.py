import datetime

from django.db import models

from proyecto_boneo.apps.administracion.personal.models import Persona, PersonaLegajo
from proyecto_boneo.apps.administracion.planes.models import InstanciaCursado, Division
from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo


class Responsable(Persona):
    usuario = models.OneToOneField(UsuarioBoneo, related_name='responsable')


class Alumno(PersonaLegajo):
    PROMEDIO_UPDATE_THRESHOLD = 3600
    usuario = models.OneToOneField(UsuarioBoneo, related_name='alumno')
    responsable = models.ForeignKey(Responsable, related_name='alumnos', on_delete=models.PROTECT)
    division = models.ForeignKey(Division, related_name='alumnos', null=True, blank=True)
    _promedio = models.FloatField(null=True, blank=True)
    last_promedio_date = models.DateTimeField(null=True, blank=True)

    def crear_usuario(self, email):
        super(Alumno, self).crear_usuario(email)
        self.usuario.is_alumno = True
        self.usuario.save()

    def calcular_promedio(self):
        inscripciones = InscripcionAlumno.objects.filter(alumno=self, instancia_cursado__division=self.division).all()
        if inscripciones:
            self._promedio = round(sum([i.promedio for i in inscripciones]) / len(inscripciones), 2)
            self.save()

    @property
    def promedio(self):
        if (not self.last_promedio_date or
                (datetime.datetime.now() - self.last_promedio_date).seconds > self.PROMEDIO_UPDATE_THRESHOLD):
            self.calcular_promedio()
        return self._promedio


class InscripcionAlumno(models.Model):
    PROMEDIO_UPDATE_THRESHOLD = 1500
    alumno = models.ForeignKey(Alumno, related_name='inscripciones')
    instancia_cursado = models.ForeignKey(InstanciaCursado, related_name='inscripciones')
    _promedio = models.FloatField(null=True, blank=True)
    last_promedio_date = models.DateTimeField(null=True, blank=True)

    def calcular_promedio(self):
        from proyecto_boneo.apps.aula_virtual.clases.models import ClaseVirtual, ResultadoEvaluacion
        evaluaciones = ResultadoEvaluacion.objects.filter(alumno=self.alumno,
                                                          clase_virtual__materia=self.instancia_cursado.materia,
                                                          clase_virtual__tipo__in=[ClaseVirtual.EVALUACION,
                                                                                   ClaseVirtual.EVALUACION_ESCRITA])
        self._promedio = round(evaluaciones.aggregate(models.Avg('nota')), 2)
        self.last_promedio_date = datetime.datetime.now()
        self.save()

    @property
    def promedio(self):
        if (not self.last_promedio_date or
                (datetime.datetime.now() - self.last_promedio_date).seconds > self.PROMEDIO_UPDATE_THRESHOLD):
            self.calcular_promedio()
        return self._promedio


class Asistencia(models.Model):
    fecha = models.DateField()
    alumno = models.ForeignKey(Alumno, related_name='asistencias')
    division = models.ForeignKey(Division, related_name='asistentes')
    asistio = models.BooleanField(default=False)
