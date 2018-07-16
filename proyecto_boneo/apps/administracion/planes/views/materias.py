import datetime

from proyecto_boneo.apps.gutils.django.views import CreateView, UpdateView, ProtectedDeleteView, FilteredReportListView, View, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render

from .. import forms, models, reports
from proyecto_boneo.apps.administracion.planes.forms import ConfigurarMateriasProfesoresFormset


class MateriasFilteredListView(FilteredReportListView):
    form_class = forms.MateriaFilterForm
    model = models.Materia
    template_name = 'planes/materias/materias_list.html'
    report = reports.MateriasReport


class MateriasCreateView(CreateView):
    model = models.Materia
    success_url = reverse_lazy('administracion:materias')
    form_class = forms.MateriaForm
    template_name = 'planes/materias/materias_form.html'


class MateriasUpdateView(UpdateView):
    model = models.Materia
    success_url = reverse_lazy('administracion:materias')
    form_class = forms.MateriaForm
    template_name = 'planes/materias/materias_form.html'


class MateriasDeleteView(ProtectedDeleteView):
    model = models.Materia
    success_url = reverse_lazy('administracion:materias')
    template_name = 'planes/materias/materias_confirm_delete.html'


class MateriasAyudaTemplateView(TemplateView):
    template_name = 'planes/materias/materias_ayuda_list.html'


class MateriasAyudaNuevoTemplateView(TemplateView):
    template_name = 'planes/materias/materias_ayuda_nuevo.html'


class MateriasAyudaEditarTemplateView(TemplateView):
    template_name = 'planes/materias/materias_ayuda_editar.html'


class MateriasAyudaEliminarTemplateView(TemplateView):
    template_name = 'planes/materias/materias_ayuda_eliminar.html'


class ConfigurarProfesoresMateriasView(View):
    template_name = 'planes/profesores_materias/profesores_materias_configurar.html'
    necesario_generar_template_name = 'planes/profesores_materias/necesario_generar_instancias.html'
    success_url = reverse_lazy('administracion:divisiones')

    def get_context_data(self, request):
        division = models.Division.objects.filter(pk=self.kwargs['pk']).first()
        instancia_cursado_list = models.InstanciaCursado.objects.año_actual().filter(division__pk=self.kwargs['pk'])
        if request.method == 'GET':
            formset = ConfigurarMateriasProfesoresFormset(queryset=instancia_cursado_list)
        else:
            formset = forms.ConfigurarMateriasProfesoresFormset(request.POST)
        context = {'formset': formset, 'division':division}
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
        for form in context['formset']:
            if not form.is_valid():
                valido= False
        return valido

    def save_formsets(self, context):
        formset = context['formset']
        formset.save()

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


class ProfesoresDivisionAyudaTemplateView(TemplateView):
    template_name = 'planes/profesores_materias/divisiones_ayuda_profesores.html'


