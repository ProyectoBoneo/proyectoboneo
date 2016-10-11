from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from proyecto_boneo.apps.administracion.usuarios.customViews.views import View

from proyecto_boneo.apps.administracion.alumnos.models import Alumno

from . import reports


class EstadoAcademicoView(View):
    template_name = 'perfil_academico/estado_academico.html'

    def check_permissions(self, request, alumno):
        return (request.user.is_staff or request.user.is_profesor or
                (request.user.is_alumno and request.user.alumno == alumno))

    def get_context_data(self):
        return {
            'alumno': self.alumno,
            'inscripciones': self.alumno.inscripciones.filter(instancia_cursado__division=self.alumno.division)
        }

    def get(self, request, alumno_pk):
        self.alumno = get_object_or_404(Alumno, pk=alumno_pk)
        if self.check_permissions(request, self.alumno):
            return render(request, self.template_name, self.get_context_data())
        else:
            raise PermissionDenied

class EstadoAcademicoReportView(View):
    report = reports.EstadoAcademicoReport

    def check_permissions(self, request, alumno):
        return (request.user.is_staff or request.user.is_profesor or
                (request.user.is_alumno and request.user.alumno == alumno))

    def get_context_data(self):
        return {
            'alumno': self.alumno,
            'inscripciones': self.alumno.inscripciones.filter(instancia_cursado__division=self.alumno.division)
        }

    def get(self, request, alumno_pk):
        self.alumno = get_object_or_404(Alumno, pk=alumno_pk)
        if self.check_permissions(request, self.alumno):
            report = self.report(self.alumno)
            filename = 'estado_academico_{}_{}'.format(self.alumno.apellido, self.alumno.nombre).replace(' ', '')
            return report.render_pdf_report(self.get_context_data(), filename)
        else:
            raise PermissionDenied

class EstadoAcademicoView(View):
    template_name = 'perfil_academico/estado_academico.html'

    def check_permissions(self, request, alumno):
        return (request.user.is_staff or request.user.is_profesor or
                (request.user.is_alumno and request.user.alumno == alumno))

    def get_context_data(self):
        return {
            'alumno': self.alumno,
            'inscripciones': self.alumno.inscripciones.filter(instancia_cursado__division=self.alumno.division),
        }

    def get(self, request, alumno_pk):
        self.alumno = get_object_or_404(Alumno, pk=alumno_pk)
        if self.check_permissions(request, self.alumno):
            return render(request, self.template_name, self.get_context_data())
        else:
            raise PermissionDenied