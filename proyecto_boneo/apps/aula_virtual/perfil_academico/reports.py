from gutils.reports import BaseModelReport
from proyecto_boneo.apps.administracion.alumnos.models import InscripcionAlumno


class EstadoAcademicoReport(BaseModelReport):
    model = InscripcionAlumno
    fields = ['instancia_cursado', 'promedio']
    headers = {'instancia_cursado': 'Materia', 'promedio': 'Promedio'}
    models_per_page = 35

    def __init__(self, alumno):
        self.alumno = alumno

    def get_base_queryset(self):
        return InscripcionAlumno.objects.filter(alumno=self.alumno,
                                                instancia_cursado__division=self.alumno.division)

    def get_page_title(self):
        return 'Estado Académico: {}, {} - Promedio General: {}'.format(self.alumno.apellido,
                                                                        self.alumno.nombre, self.alumno.promedio)
