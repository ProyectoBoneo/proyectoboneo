from datetime import datetime
from gutils.django.views import ProtectedDeleteView, FilteredReportListView, View
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render

from proyecto_boneo.apps.administracion.personal.views import PersonaCreateView, PersonaUpdateView

from proyecto_boneo.apps.administracion.alumnos.models import InscripcionAlumno, Asistencia, Alumno

from . import forms, models, reports


#region Alumnos
class AlumnosFilteredListView(FilteredReportListView):
    form_class = forms.AlumnoFilterForm
    model = models.Alumno
    template_name = 'alumnos/alumnos/alumnos_list.html'
    report = reports.AlumnosReport

    
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


class AlumnosInscripcionesView(View):
    template_name = 'alumnos/alumnos/alumnos_inscripciones.html'

    def get_context_data(self, request):
        division_query = models.Division.objects.filter(pk=self.kwargs['pk'])
        division = division_query.first()
        context = None
        if request.method == 'POST':
            formset = forms.InscripcionesAlumnoFormset(request.POST)
            context = {
               'formset': formset,
               'division': division
            }
        if request.method == 'GET':
            alumno_list = division_query.first().alumnos.all()
            alumno_form_list = []
            if alumno_list != None and alumno_list.exists() and request.method == 'GET':
                for alumno in alumno_list:
                    alumno_form_list.append({'alumno': alumno.id})
            formset = forms.InscripcionesAlumnoFormset(initial=alumno_form_list)
            context = {
                       'formset': formset,
                       'division': division
            }
        return context

    def get(self, request, *args, **kwargs):
            return render(request, self.template_name, self.get_context_data(request))

    def validate_formsets(self, context):
        valido = True
        formset = context['formset']
        for form in formset:
            if not form.is_valid():
                valido= False
        return valido

    def save_formsets(self, context):
        division = context['division']
        formset = context['formset']
        for form in formset:
            if form.has_changed() and 'alumno' in form.cleaned_data and form.cleaned_data['alumno'] is not None:
                alumno = Alumno.objects.filter(id=form.cleaned_data['alumno'].id).first()
                for instancia_cursado in division.instancias_cursado.filter(anio_cursado=datetime.today().year).all():
                    inscripcion_alumno, created = InscripcionAlumno.objects.get_or_create(alumno=alumno,
                                                     instancia_cursado=instancia_cursado)
                if division != alumno.division:
                    alumno.division = division
                    alumno.save()
        for formToDelete in formset.deleted_forms:
            if 'alumno' in formToDelete.cleaned_data and formToDelete.cleaned_data['alumno'] is not None:
                alumno = Alumno.objects.filter(id=formToDelete.cleaned_data['alumno'].id).first()
                for instancia_cursado in division.instancias_cursado.filter(anio_cursado=datetime.today().year).all():
                    inscripcion_alumno_borrar = InscripcionAlumno.objects.get(alumno=alumno,
                                                     instancia_cursado=instancia_cursado)
                    inscripcion_alumno_borrar.delete()
                alumno.division = None
                alumno.save()

    def post(self, request, *args, **kwargs):
        mode = request.POST.get('mode-field')

        context = self.get_context_data(request)
        if mode=='confirmar':
           success_url = reverse_lazy('administracion:divisiones')
        else:
           success_url = reverse_lazy('administracion:inscripciones_alumno', kwargs={'pk':context['division'].id})
        if self.validate_formsets(context):
            self.save_formsets(context)
            return redirect(success_url)
        else:
            return render(request, self.template_name, context)

#endregion


#region Responsables
class ResponsablesFilteredListView(FilteredReportListView):
    form_class = forms.ResponsableFilterForm
    model = models.Responsable
    template_name = 'alumnos/responsables/responsables_list.html'
    report = reports.ResponsablesReport


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
        division = models.Division.objects.filter(pk=self.kwargs['pk']).first()
        instancia_cursado = division.instancias_cursado.filter(anio_cursado=self.fechaAIngresar.year).first()
        alumno_list = []
        asistencia_list = models.Asistencia.objects.filter(division=division).filter(fecha=self.fechaAIngresar).all()
        if asistencia_list != None and asistencia_list.exists() and request.method == 'GET':
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
                   'alumno_list': alumno_list,
                   'division':division,
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
         division = context['division']
         for alumno in context['alumno_list']:
            formset = alumno['formset']
            for form in formset:
                if 'id' in form.cleaned_data and form.cleaned_data['id'] is not None:
                    asistencia = Asistencia.objects.filter(id=form.cleaned_data['id']).first()
                else:
                    asistencia = Asistencia()
                asistencia.division = division
                asistencia.fecha = self.fechaAIngresar
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
