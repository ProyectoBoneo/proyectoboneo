from gutils.django.views import ProtectedDeleteView, FilteredListView, ModelFormsetView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404

from proyecto_boneo.apps.administracion.personal.views import PersonaCreateView, PersonaUpdateView

from proyecto_boneo.apps.administracion.alumnos.models import InscripcionAlumno

from . import forms, models


#region Alumnos
class AlumnosFilteredListView(FilteredListView):
    form_class = forms.AlumnoFilterForm
    model = models.Alumno
    template_name = 'alumnos/alumnos/alumnos_list.html'
    
    
class AlumnosCreateView(PersonaCreateView):
    model = models.Alumno
    success_url = reverse_lazy('administracion:alumnos')
    form_class = forms.AlumnoForm
    template_name = 'alumnos/alumnos/alumnos_form.html'


class AlumnosUpdateView(PersonaUpdateView):
    model = models.Alumno
    success_url = reverse_lazy('administracion:alumnos')
    form_class = forms.AlumnoForm
    template_name = 'alumnos/alumnos/alumnos_form.html'


class AlumnosDeleteView(ProtectedDeleteView):
    model = models.Alumno
    success_url = reverse_lazy('administracion:alumnos')
    template_name = 'alumnos/alumnos/alumnos_confirm_delete.html'


class AlumnosInscripcionesView(ModelFormsetView):
    template_name = 'alumnos/alumnos/alumnos_inscripciones.html'
    formset = forms.InscripcionesFormset

    def __init__(self, **kwargs):
        self._alumno = None
        super(AlumnosInscripcionesView, self).__init__(**kwargs)

    @property
    def alumno(self):
        if not self._alumno:
            self._alumno = get_object_or_404(models.Alumno, pk=self.kwargs['pk'])
        return self._alumno

    def get_context_data(self, *args, **kwargs):
        context = super(AlumnosInscripcionesView, self).get_context_data(*args, **kwargs)
        context['alumno'] = self.alumno
        return context

    def get_queryset(self):
        return InscripcionAlumno.objects.filter(alumno=self.alumno)
#endregion


#region Responsables
class ResponsablesFilteredListView(FilteredListView):
    form_class = forms.ResponsableFilterForm
    model = models.Responsable
    template_name = 'alumnos/responsables/responsables_list.html'


class ResponsablesCreateView(PersonaCreateView):
    model = models.Responsable
    success_url = reverse_lazy('administracion:responsables')
    form_class = forms.ResponsableForm
    template_name = 'alumnos/responsables/responsables_form.html'


class ResponsablesUpdateView(PersonaUpdateView):
    model = models.Responsable
    success_url = reverse_lazy('administracion:responsables')
    form_class = forms.ResponsableForm
    template_name = 'alumnos/responsables/responsables_form.html'


class ResponsablesDeleteView(ProtectedDeleteView):
    model = models.Responsable
    success_url = reverse_lazy('administracion:responsables')
    template_name = 'alumnos/responsables/responsables_confirm_delete.html'
#endregion

