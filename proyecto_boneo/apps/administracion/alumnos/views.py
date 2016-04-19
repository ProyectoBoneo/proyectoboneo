from datetime import date
from gutils.django.views import ProtectedDeleteView, FilteredListView, ModelFormsetView, View
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render

from proyecto_boneo.apps.administracion.personal.views import PersonaCreateView, PersonaUpdateView

from proyecto_boneo.apps.administracion.alumnos.models import InscripcionAlumno

from . import forms, models


#region Alumnos
from proyecto_boneo.apps.administracion.planes.models import Horario


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


#region Asistencia
class AsistenciaView(View):
    template_name = 'alumnos/asistencias/asistencias_form.html'
    success_url = reverse_lazy('administracion:divisiones')

    def get_context_data(self, request):
        horario = Horario.objects.filter(pk=self.kwargs['pk']).first()
        instancia_cursado = horario.instancia_cursado
        alumno_list = []
        # TODO: Si no existen inscripciones indicar que no puede tomarse asistencia
        for inscripcion in instancia_cursado.inscripciones.all():
            prefix = str(inscripcion.alumno.id)
            initial=[{
                'alumno_id': inscripcion.alumno.id,
                'horario_id': horario.id,
                'fecha': date.today(),
                'asistio': False
            }]
            formset = forms.AsistenciaFormset(initial=initial,
                                              prefix=prefix)
            alumno_list.append({'alumno':inscripcion.alumno,
                                'formset': formset})

        context = {'alumno_list': alumno_list}
        return context

    def get(self, request, *args, **kwargs):
            return render(request, self.template_name, self.get_context_data(request))


    def validate_formsets(self, context):
        valido = True
        for dia_semana in context['dias_semana']:
            for form in dia_semana['formset']:
                if not form.is_valid():
                    valido= False
        return valido

    def save_formsets(self, context):
        # TODO: El post debe tomar los formsets, guardar primero la clase real que corresponde a este horario,
        # y luego guardar la asistencia relacionada a esa clase real para cada alumno.
        for dia_semana in context['dias_semana']:
            formset = dia_semana['formset']
            for formToDelete in formset.deleted_forms:
                if('hora_inicio' in formToDelete.cleaned_data
                and 'hora_fin' in formToDelete.cleaned_data
                and formToDelete.cleaned_data['hora_inicio'] != None
                and formToDelete.cleaned_data['hora_fin'] != None
                and formToDelete.cleaned_data['id'] != None):
                    horario = Horario.objects.get(id=formToDelete.cleaned_data['id'])
                    horario.delete()
            for form in formset:
                if('hora_inicio' in form.cleaned_data
                and 'hora_fin' in form.cleaned_data
                and form.cleaned_data['hora_inicio'] is not None
                and form.cleaned_data['hora_fin'] is not None
                and form.cleaned_data['DELETE'] != True):
                    if(form.cleaned_data['id']):
                        horario = Horario.objects.get(id=form.cleaned_data['id'])
                    else:
                        horario = Horario()
                    instancia_cursado = models.InstanciaCursado.objects.año_actual().filter(division__pk=self.kwargs['pk'],
                                                                        materia=form.cleaned_data['materia']).first()
                    horario.instancia_cursado = instancia_cursado
                    horario.hora_inicio = form.cleaned_data['hora_inicio']
                    horario.hora_fin = form.cleaned_data['hora_fin']
                    horario.dia_semana = form.cleaned_data['dia_semana']
                    horario.save()

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        if self.validate_formsets(context):
            self.save_formsets(context)
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, context)
#endregion
