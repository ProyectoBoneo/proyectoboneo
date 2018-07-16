import datetime

from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from proyecto_boneo.apps.administracion.planes.models import Horario
from proyecto_boneo.apps.administracion.tutorias.models import EncuentroTutoria
from proyecto_boneo.apps.aula_virtual.biblioteca.models import Material
from proyecto_boneo.apps.aula_virtual.clases.models import ClaseVirtual


def home_redirect_router(request, *args, **kwargs):
    if request.user.is_staff:
        return StaffHomeView.as_view()(request, *args, **kwargs)
    elif request.user.is_alumno:
        return AlumnoHomeView.as_view()(request, *args, **kwargs)
    elif request.user.is_profesor:
        return ProfesorHomeView.as_view()(request, *args, **kwargs)
    else:
        return redirect(reverse('aula_virtual:home'))
    pass


class StaffHomeView(TemplateView):
    template_name = 'home/home.html'

class AlumnoHomeView(TemplateView):
    template_name = 'home/alumno_home.html'

    def get_context_data(self, **kwargs):
        context = super(AlumnoHomeView, self).get_context_data(**kwargs)
        context['horarios'] = Horario.objects\
            .filter(instancia_cursado__inscripciones__alumno=self.request.user.alumno).distinct()
        context['clases_no_respondidas'] = ClaseVirtual.objects\
            .filter(materia__instancias_cursado__inscripciones__alumno=self.request.user.alumno)\
            .exclude(tipo='esc').exclude(respuestas__alumno=self.request.user.alumno).distinct()
        context['ultimos_materiales'] = Material.objects\
            .filter(materia__instancias_cursado__inscripciones__alumno=self.request.user.alumno).distinct()
        context['encuentros_tutorias'] = EncuentroTutoria.objects\
            .filter(tutoria__alumno=self.request.user.alumno).filter(tutoria__anio = datetime.datetime.today().year).distinct()
        context['proximos_encuentros_tutorias'] = EncuentroTutoria.objects\
            .filter(tutoria__alumno=self.request.user.alumno).filter(tutoria__anio = datetime.datetime.today().year)\
            .filter(fecha__gte = datetime.datetime.now()).distinct()
        return context


class ProfesorHomeView(TemplateView):
     template_name = 'home/profesor_home.html'

     def get_context_data(self, **kwargs):
        context = super(ProfesorHomeView, self).get_context_data(**kwargs)
        context['horarios'] = Horario.objects\
            .filter(instancia_cursado__profesor_titular=self.request.user.profesor).distinct()
        # context['clases_no_respondidas'] = ClaseVirtual.objects\
        #     .filter(materia__instancias_cursado__inscripciones__alumno=self.request.user.alumno)\
        #     .exclude(respuestas__alumno=self.request.user.alumno).distinct()
        # context['ultimos_materiales'] = Material.objects\
        #     .filter(materia__instancias_cursado__inscripciones__alumno=self.request.user.alumno).distinct()
        context['encuentros_tutorias'] = EncuentroTutoria.objects\
            .filter(tutoria__profesor=self.request.user.profesor).filter(tutoria__anio = datetime.datetime.today().year).distinct()
        context['proximos_encuentros_tutorias'] = EncuentroTutoria.objects\
            .filter(tutoria__profesor=self.request.user.profesor).filter(tutoria__anio = datetime.datetime.today().year)\
            .filter(fecha__gte = datetime.datetime.now()).distinct()
        return context


class IndiceView(TemplateView):
     template_name = 'ayuda//indice.html'

class ProximosEncuentrosTutoriaAyudaTemplateView(TemplateView):
    template_name = 'ayuda/home/proximos_encuentros.html'

class NuevasClasesVirtualesAyudaTemplateView(TemplateView):
    template_name = 'ayuda/home/nuevas_clases_virtuales.html'

class CalendarioAyudaTemplateView(TemplateView):
    template_name = 'ayuda/home/calendario.html'
