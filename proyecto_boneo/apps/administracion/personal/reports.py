from proyecto_boneo.apps.gutils.reports import BaseModelReport
from proyecto_boneo.apps.administracion.personal.models import Profesor


class ProfesoresReport(BaseModelReport):
    model = Profesor
    fields = ['apellido', 'nombre', 'dni', 'domicilio']
    widths = {'domicilio': 40}
    title = 'Profesores'
    ordering = ('apellido', 'nombre')
    models_per_page = 35
