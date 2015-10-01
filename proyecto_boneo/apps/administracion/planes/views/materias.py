import datetime

from gutils.django.views import CreateView, UpdateView, ProtectedDeleteView, FilteredListView, View
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render

from .. import forms, models


class MateriasFilteredListView(FilteredListView):
    form_class = forms.MateriaFilterForm
    model = models.Materia
    template_name = 'planes/materias/materias_list.html'


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


class ConfigurarProfesoresMateriasView(View):
    template_name = 'planes/profesores_materias/profesores_materias_configurar.html'
    necesario_generar_template_name = 'planes/profesores_materias/necesario_generar_instancias.html'
    success_url = reverse_lazy('administracion:divisiones')

    def _necesario_generar_instancias_response(self, request):
        context = {}
        return render(request, self.necesario_generar_template_name,
                      context)

    def get_context_data(self, request):
        estructura_plan = models.Division.objects.estructura_plan()
        anio_cursado = datetime.date.today().year
        for año in estructura_plan:
            for materia in año['materias']:
                prefix = str(materia['materia'].id)
                if request.method == 'GET':
                    initial = []
                    for div in materia['divisiones']:
                        instancia_cursado = models.InstanciaCursado.objects.get(division=div,
                                                                                materia=materia['materia'],
                                                                                anio_cursado=anio_cursado)
                        profesor = instancia_cursado.profesor_titular
                        initial_data = {'instancia_cursado': instancia_cursado, 'profesor': profesor}
                        initial.append(initial_data)
                    materia['formset'] = forms.ConfigurarMateriasProfesoresFormset(initial=initial,
                                                                                   prefix=prefix)
                else:
                    materia['formset'] = forms.ConfigurarMateriasProfesoresFormset(request.POST,
                                                                                   prefix=prefix)
        context = {'estructura_plan': estructura_plan}
        return context

    def get(self, request, *args, **kwargs):
        if models.InstanciaCursado.objects.necesario_generar():
            return self._necesario_generar_instancias_response(request)
        else:
            return render(request, self.template_name, self.get_context_data(request))

    def validate_formsets(self, context):
        valido = True
        for año in context['estructura_plan']:
            for materia in año['materias']:
                if not materia['formset'].is_valid():
                    valido = False
        return valido

    def save_formsets(self, context):
        for año in context['estructura_plan']:
            for materia in año['materias']:
                formset = materia['formset']
                for form in formset:
                    instancia_cursado = form.cleaned_data['instancia_cursado']
                    instancia_cursado.profesor_titular = form.cleaned_data['profesor']
                    instancia_cursado.save()

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
