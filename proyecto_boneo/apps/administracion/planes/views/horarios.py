from datetime import datetime
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView
from gutils.django.views import View
from .. import forms, models
from proyecto_boneo.apps.administracion.planes.forms import ConfigurarHorariosMateriasForm, HorarioFechaForm
from proyecto_boneo.apps.administracion.planes.models import Horario

DIAS_SEMANA_CHOICES = [(1,"Lunes"), (2,"Martes"), (3,"Miercoles"), (4,"Jueves"),
                       (5,"Viernes"), (6,"Sabado"), (7, "Domingo")]

class ConfigurarHorariosDivisionView(View):
    template_name = 'planes/horarios_materias/horarios_materias_configurar.html'
    necesario_generar_template_name = 'planes/horarios_materias/necesario_generar_instancias.html'
    success_url = reverse_lazy('administracion:divisiones')

    def get_context_data(self, request):
        division = models.Division.objects.filter(pk=self.kwargs['pk']).first()
        instancia_cursado = models.InstanciaCursado.objects.año_actual().filter(division__pk=self.kwargs['pk'])
        dias_semana = []
        for dia_semana in models.Horario.objects.get_dias_semana_choices()[0:6]:
            dia_semana_id=dia_semana[0]
            prefix = str(dia_semana_id)
            if request.method == 'GET':
                horarios_existentes = Horario.objects.filter(instancia_cursado = instancia_cursado)\
                    .filter(dia_semana=dia_semana_id)
                if horarios_existentes.exists():
                    initial = []
                    for horario in horarios_existentes.all():
                        initial.append({
                            'dia_semana': horario.dia_semana,
                            'materia': horario.instancia_cursado.materia.pk,
                            'id': horario.id,
                            'hora_inicio': horario.hora_inicio,
                            'hora_fin': horario.hora_fin
                        })
                else:
                    initial = [{'dia_semana': dia_semana_id,
                               }]
                formset = forms.ConfigurarMateriasHorariosFormset(initial=initial,
                                                                    prefix=prefix)
            else:
                formset = forms.ConfigurarMateriasHorariosFormset(request.POST,
                                                                    prefix=prefix)
            dias_semana.append({'dia_id':dia_semana_id,
                                'dia_descripcion': dia_semana[1],
                                'formset': formset})

        context = {'dias_semana': dias_semana,
                   'division': division}
        return context

    def get(self, request, *args, **kwargs):
        if models.InstanciaCursado.objects.necesario_generar():
            return self._necesario_generar_instancias_response(request)
        else:
            return render(request, self.template_name, self.get_context_data(request))

    def _necesario_generar_instancias_response(self, request):
        context = {}
        return render(request, self.necesario_generar_template_name,
                      context)

    def validate_formsets(self, context):
        valido = True
        for dia_semana in context['dias_semana']:
            for form in dia_semana['formset']:
                if not form.is_valid():
                    valido= False
        return valido

    def save_formsets(self, context):
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
        if models.InstanciaCursado.objects.necesario_generar():
            return self._necesario_generar_instancias_response(request)
        else:
            context = self.get_context_data(request)
            if self.validate_formsets(context):
                self.save_formsets(context)
                return redirect(self.success_url)
            else:
                return render(request, self.template_name, context)


class HorarioPorFechaView(ListView):
    template_name = 'planes/horarios/horarios_por_fecha.html'

    def get_queryset(self):
        dia_semana = self.get_fecha().weekday()
        divisiones = models.Division.objects.filter(instancias_cursado__horarios__dia_semana=dia_semana)\
            .order_by('id').distinct('id')
        return divisiones
        # return models.Horario.objects.filter(dia_semana=dia_semana)

    def get_context_data(self, **kwargs):
        context = super(HorarioPorFechaView, self).get_context_data(**kwargs)
        initial = {'fecha': self.get_fecha()}
        fecha_form = HorarioFechaForm(initial = initial)
        context['fecha_form'] = fecha_form
        return context

    def get_fecha(self):
        if 'year' in self.kwargs and 'month' in self.kwargs and 'year' in self.kwargs:
            year = int(self.kwargs['year'])
            month = int(self.kwargs['month'])
            day = int(self.kwargs['day'])
            dt = datetime(year=year, month=month, day=day)
        else:
            dt = datetime.today()
        return dt


class HorarioIrAFechaView(View):
    def post(self, request):
        form = HorarioFechaForm(self.request.POST)
        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            url = reverse_lazy('administracion:horario_por_fecha',
                kwargs={'day': fecha.day, 'month': fecha.month, 'year': fecha.year})
            return HttpResponseRedirect(url)
