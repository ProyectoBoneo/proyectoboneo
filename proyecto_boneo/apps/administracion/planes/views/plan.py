from gutils.django.views import View, ListView, TemplateView
from django.core.urlresolvers import reverse_lazy

from django.shortcuts import render, redirect

from .. import forms, models


class DivisionesListView(ListView):
    model = models.Division
    template_name = 'planes/divisiones/divisiones_list.html'

    def get_context_data(self, **kwargs):
        context = super(DivisionesListView, self).get_context_data(**kwargs)
        try:
            año_lectivo = models.InstanciaCursado.objects.values(
                'anio_cursado').latest('anio_cursado')['anio_cursado']
        except models.InstanciaCursado.DoesNotExist:
            año_lectivo = None
        es_necesario_generar_instancias = models.InstanciaCursado.objects.necesario_generar()
        context['anio_lectivo'] = año_lectivo
        context['necesario_generar'] = es_necesario_generar_instancias
        return context

    def get_queryset(self):
        return models.Division.objects.filter(activa=True).order_by('anio', 'letra')


class DivisionesConfigurationView(View):
    template_name = 'planes/divisiones/divisiones_configurar.html'
    success_url = reverse_lazy('administracion:divisiones')

    def get(self, request, *args, **kwargs):
        context = {'cantidad_anios_form': self._get_form(),
                   'cantidad_divisiones_formset': self._get_formset()}
        return render(request, self.template_name, context)

    def _get_form(self):
        años_actuales = models.Division.objects.filter(
            activa=True).order_by('anio').values('anio').distinct()
        cantidad_años = len(años_actuales)
        if not cantidad_años:
            cantidad_años = 1
        return forms.ConfigurarCantidadAniosForm(initial={'cantidad_anios': cantidad_años})

    def _get_formset(self):
        años_actuales = models.Division.objects.filter(
            activa=True).order_by('anio').values('anio').distinct()
        initial = []
        for año_value in años_actuales:
            año = año_value['anio']
            cantidad_divisiones = len(models.Division.objects.filter(anio=año))
            initial.append({'anio': año, 'cantidad_divisiones': cantidad_divisiones})
        if not initial:
            initial.append({'año': 1, 'cantidad_divisiones': 1})
        formset = forms.CantidadDivisionesFormset(initial=initial)
        return formset

    def _proccess_formset(self, formset):
        for form in formset:
            año = form.cleaned_data.get('anio')
            cantidad_divisiones = form.cleaned_data.get('cantidad_divisiones')
            if año and cantidad_divisiones:
                models.Division.objects.configurar_divisiones_año(año, cantidad_divisiones)

    def post(self, request, *args, **kwargs):
        cantidad_anios_form = forms.ConfigurarCantidadAniosForm(request.POST)
        cantidad_divisiones_formset = forms.CantidadDivisionesFormset(request.POST)
        if cantidad_anios_form.is_valid() and cantidad_divisiones_formset.is_valid():
            self._proccess_formset(cantidad_divisiones_formset)
            return redirect(self.success_url)
        else:
            context = {'cantidad_anios_form': cantidad_anios_form,
                       'cantidad_divisiones_formset': cantidad_divisiones_formset, }
            return render(request, self.template_name, context)


class DivisionesGenerarInstanciasCursadoView(View):

    confirm_template_name = 'planes/instancias_cursado/instancias_cursado_confirm_generar.html'
    no_needed_template_name = 'planes/instancias_cursado/instancias_cursado_no_necesarias.html'
    success_template_name = 'planes/instancias_cursado/instancias_cursado_generadas.html'

    def get(self, request, *args,  **kwargs):
        ctx = {}
        if models.InstanciaCursado.objects.necesario_generar():
            return render(request, self.confirm_template_name, ctx)
        else:
            return self._instancias_no_necesarias_response(request)

    def _instancias_no_necesarias_response(self, request):
        ctx = {}
        return render(request, self.no_needed_template_name, ctx)

    def _generar_instancias_cursado(self):
        models.InstanciaCursado.objects.generar_año_actual()

    def post(self, request, *args, **kwargs):
        if models.InstanciaCursado.objects.necesario_generar():
            self._generar_instancias_cursado()
            ctx = {}
            return render(request, self.success_template_name,ctx)
        else:
            return self._instancias_no_necesarias_response(request)


class DivisionesAyudaTemplateView(TemplateView):
    template_name = 'planes/divisiones/divisiones_ayuda_list.html'