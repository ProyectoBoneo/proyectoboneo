from datetime import date, datetime, timedelta
from gutils.django.views import ProtectedDeleteView, FilteredListView, ModelFormsetView, View
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render

from proyecto_boneo.apps.administracion.personal.views import PersonaCreateView, PersonaUpdateView

from proyecto_boneo.apps.administracion.alumnos.models import InscripcionAlumno, Asistencia, Alumno

from . import forms, models


#region Alumnos
from proyecto_boneo.apps.administracion.planes.models import Horario, ClaseReal


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
    fechaAIngresar = None

    def get_fecha(self):
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        day = int(self.kwargs['day'])
        dt = datetime(year=year, month=month, day=day)
        return dt

    def get_context_data(self, request):
        self.fechaAIngresar = self.get_fecha()
        horario = Horario.objects.filter(pk=self.kwargs['pk']).first()
        if horario.dia_semana != self.fechaAIngresar.weekday():
            return {}
        instancia_cursado = horario.instancia_cursado
        alumno_list = []
        clase_real_query = ClaseReal.objects.filter(horario=horario).filter(fecha=self.fechaAIngresar)
        if clase_real_query.exists():
            clase_real = clase_real_query.first()
        else:
            clase_real = None
        if clase_real != None and clase_real.asistentes.exists() and request.method == 'GET':
            asistencia_list = models.Asistencia.objects.filter(clase_real=clase_real).all()
            for asistencia in asistencia_list :
                prefix = str(asistencia.alumno.id)
                initial =[{
                    'id': asistencia.id,
                    'alumno_id': asistencia.alumno.id,
                    'asistio': asistencia.asistio
                }]
                formset = forms.AsistenciaFormset(initial=initial,
                              prefix=prefix)
                alumno_list.append({
                    'alumno':asistencia.alumno,
                    'formset': formset})
        else:
            for inscripcion in instancia_cursado.inscripciones.all():
                prefix = str(inscripcion.alumno.id)
                if request.method == 'GET':
                    initial=[{
                        'alumno_id': inscripcion.alumno.id,
                        'asistio': False
                    }]
                    formset = forms.AsistenciaFormset(initial=initial,
                                                  prefix=prefix)
                else:
                    formset = forms.AsistenciaFormset(request.POST,
                                                      prefix=prefix)
                alumno_list.append({
                                    'alumno':inscripcion.alumno,
                                    'formset': formset})

        context = {
                   'clase_real': clase_real,
                   'alumno_list': alumno_list,
                   'horario':horario,
                    'instancia_cursado':instancia_cursado,
                    'fecha': self.get_fecha()
        }
        return context

    def get(self, request, *args, **kwargs):
            return render(request, self.template_name, self.get_context_data(request))


    def validate_formsets(self, context):
        valido = True
        for alumno in context['alumno_list']:
            for form in alumno['formset']:
                if not form.is_valid():
                    valido= False
        return valido

    def save_formsets(self, context):
         instancia_cursado = context['instancia_cursado']
         horario = context['horario']
         if not context['clase_real']:
            clase_real = ClaseReal()
         else:
            clase_real = context['clase_real']
         clase_real.instancia_cursado = instancia_cursado
         clase_real.horario = horario
         clase_real.fecha = self.fechaAIngresar
         clase_real.hora_inicio = horario.hora_inicio
         clase_real.hora_fin = horario.hora_fin
         clase_real.save()
         for alumno in context['alumno_list']:
            formset = alumno['formset']
            for form in formset:
                if 'id' in form.cleaned_data and form.cleaned_data['id'] is not None:
                    asistencia = Asistencia.objects.filter(id=form.cleaned_data['id']).first()
                else:
                    asistencia = Asistencia()
                asistencia.clase_real = clase_real
                alumno = Alumno.objects.filter(pk=form.cleaned_data['alumno_id']).first()
                asistencia.alumno = alumno
                if 'asistio' in form.cleaned_data:
                    asistencia.asistio = form.cleaned_data['asistio']
                else:
                    asistencia.asistio = False
                asistencia.save()

    def post(self, request, *args, **kwargs):
        success_url = reverse_lazy('administracion:horario_por_fecha',
                kwargs={'day': self.get_fecha().day, 'month': self.get_fecha().month, 'year': self.get_fecha().year})
        context = self.get_context_data(request)
        if self.validate_formsets(context):
            self.save_formsets(context)
            return redirect(success_url)
        else:
            return render(request, self.template_name, context)
#endregion
