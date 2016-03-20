from gutils.django.views import CreateView, UpdateView, ProtectedDeleteView, FilteredListView, ListView
from django.core.urlresolvers import reverse_lazy

from . import forms, models
from django.views.generic import TemplateView


# class MaterialesFilteredListView(FilteredListView):
#     form_class = forms.MaterialFilterForm
#     model = models.Material
#     template_name = 'biblioteca_virtual/materiales/materiales_list.html'
#
#
from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo


class ComunicadoListView(ListView):
    form_class = forms.ComunicadoFilterForm
    model = models.Comunicado
    template_name = 'comunicados/comunicados_list.html'


class ComunicadoCreateView(CreateView):
    model = models.Comunicado
    success_url = reverse_lazy('administracion:comunicados')
    form_class = forms.ComunicadoForm
    template_name = 'comunicados/comunicados_form.html'

    def form_valid(self, form):
        form.instance.emisor = self.request.user
        return super(ComunicadoCreateView, self).form_valid(form)


class ComunicadoUpdateView(UpdateView):
    model = models.Comunicado
    success_url = reverse_lazy('administracion:comunicados')
    form_class = forms.ComunicadoForm
    template_name = 'comunicados/comunicados_form.html'


class ComunicadoDeleteView(ProtectedDeleteView):
    model = models.Comunicado
    success_url = reverse_lazy('administracion:comunicados')
    template_name = 'comunicados/comunicados_confirm_delete.html'
