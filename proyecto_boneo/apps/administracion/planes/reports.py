from gutils.reports import BaseModelReport
from proyecto_boneo.apps.administracion.planes.models import Materia


class MateriasReport(BaseModelReport):
    model = Materia
    fields = ['anio', 'descripcion', 'observaciones']
    widths = {'anio': 10, 'descripcion': 40}
    headers = {'descripcion': 'Descripción', 'anio': 'Año'}
    title = 'Materias'
    ordering = ('anio', 'descripcion')
    models_per_page = 35
