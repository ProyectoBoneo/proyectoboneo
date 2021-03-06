import string
import datetime

from django.db import models
from django.db.models import ForeignKey

from proyecto_boneo.apps.administracion.personal.models import Profesor


class Materia(models.Model):

    class Meta:
        ordering = ['anio', 'descripcion']

    descripcion = models.CharField(max_length=150)
    observaciones = models.TextField(null=True, blank=True)
    anio = models.IntegerField()

    def __str__(self):
        return '{} - {}'.format(self.anio, self.descripcion)


class DivisionManager(models.Manager):

    def años_plan(self):
        años = self.filter(activa=True).order_by('anio').values('anio').distinct('anio')
        return [año['anio'] for año in años]

    def estructura_plan(self):
        plan = []
        for año in self.años_plan():
            materias = []
            divisiones = self.filter(activa=True, anio=año)
            for materia in Materia.objects.filter(anio=año):
                materia_info = {'materia': materia,
                                'divisiones': divisiones}
                materias.append(materia_info)

            año_plan = {'anio': año,
                        'materias': materias,
                        'divisiones': divisiones}
            plan.append(año_plan)
        return plan

    def configurar_divisiones_año(self, año, cantidad_divisiones):
        divisiones_actuales = self.filter(anio=año, activa=True)
        cantidad_actual = len(divisiones_actuales)
        if cantidad_actual > cantidad_divisiones:
            letras_sobrantes = Division.LETRAS[cantidad_divisiones - 1:cantidad_actual]
            divisiones_actuales.filter(letra__in=letras_sobrantes).update(activa=False)
        elif cantidad_actual < cantidad_divisiones:
            letras_faltantes = Division.LETRAS[cantidad_actual:cantidad_divisiones]
            for letra in letras_faltantes:
                self.create(anio=año, activa=True, letra=letra)


class Division(models.Model):
    """
    Elemento de configuración del sistema. Determina cuáles son las divisiones activas
    donde se pueden inscribir los alumnos
    """

    class Meta:
        ordering = ['anio', 'letra']

    LETRAS = list(string.ascii_uppercase[:10])

    anio = models.IntegerField()
    letra = models.CharField(max_length=1, null=True, blank=True)
    activa = models.BooleanField(default=True)

    objects = DivisionManager()

    def __str__(self):
        return '{}º {}'.format(self.anio, self.letra)


class InstanciaCursadoManager(models.Manager):

    def generar_año_actual(self):
        self.generar(datetime.date.today().year)

    def generar(self, año):
        divisiones = Division.objects.filter(activa=True)
        for division in divisiones:
            materias = Materia.objects.filter(anio=division.anio)
            for materia in materias:
                self.get_or_create(division=division,
                                   materia=materia,
                                   anio_cursado=año)

    def necesario_generar(self):
        año_actual = datetime.date.today().year
        divisiones = Division.objects.filter(activa=True)
        for division in divisiones:
            materias = Materia.objects.filter(anio=division.anio)
            for materia in materias:
                try:
                    self.get(division=division,
                             materia=materia,
                             anio_cursado=año_actual)
                except InstanciaCursado.DoesNotExist:
                    return True
        return False

    def año_actual(self):
        año_actual = datetime.date.today().year
        queryset = super(InstanciaCursadoManager, self).get_queryset()
        return queryset.filter(anio_cursado=año_actual)


class InstanciaCursado(models.Model):

    objects = InstanciaCursadoManager()

    anio_cursado = models.IntegerField()
    materia = models.ForeignKey(Materia, related_name='instancias_cursado', on_delete=models.CASCADE)
    division = models.ForeignKey(Division, related_name='instancias_cursado', on_delete=models.CASCADE)
    profesor_titular = models.ForeignKey(Profesor, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} - {}'.format(self.materia.descripcion, self.division, self.anio_cursado)


class Horario(models.Model):
    DIAS_DE_SEMANA_CHOICES = [
        (0, "Lunes"),
        (1, "Martes"),
        (2, "Miercoles"),
        (3, "Jueves"),
        (4, "Viernes"),
        (5, "Sabado"),
        (6, "Domingo")
    ]

    instancia_cursado = models.ForeignKey(InstanciaCursado, related_name='horarios', on_delete=models.CASCADE)
    dia_semana = models.IntegerField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    @property
    def descripcion_dia_semana(self):
        try:
            return [descripcion for value, descripcion in self.DIAS_DE_SEMANA_CHOICES if value == self.dia_semana][0]
        except IndexError:
            return None

    def __str__(self):
        return '{} - {} - {} - {}'.format(self.instancia_cursado, self.dia_semana, self.hora_inicio, self.hora_fin)
