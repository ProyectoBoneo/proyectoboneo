from proyecto_boneo.apps.gutils.reports import BaseModelReport
from proyecto_boneo.apps.administracion.alumnos.models import Alumno, Responsable


class AlumnosReport(BaseModelReport):
    model = Alumno
    fields = ['apellido', 'nombre', 'dni', 'domicilio', 'division']
    widths = {'division': 10, 'domicilio': 30}
    headers = {'division': 'División'}
    title = 'Alumnos'
    ordering = ('apellido', 'nombre')
    models_per_page = 35


class ResponsablesReport(BaseModelReport):
    model = Responsable
    fields = ['apellido', 'nombre', 'dni', 'domicilio']
    widths = {'domicilio': 40}
    title = 'Responsables'
    ordering = ('apellido', 'nombre')
    models_per_page = 35
