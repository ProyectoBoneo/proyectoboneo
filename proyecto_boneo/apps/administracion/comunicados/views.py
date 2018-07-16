from django.shortcuts import get_object_or_404
from proyecto_boneo.apps.gutils.django.views import CreateView, UpdateView, ProtectedDeleteView, FilteredListView, ListView, DetailView
from django.urls import reverse_lazy

from . import forms, models
from django.views.generic import TemplateView


# class MaterialesFilteredListView(FilteredListView):
#     form_class = forms.MaterialFilterForm
#     model = models.Material
#     template_name = 'biblioteca_virtual/materiales/materiales_list.html'
#
#
from proyecto_boneo.apps.administracion.comunicados.models import Comunicado
from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo


class ComunicadoListView(ListView):
    form_class = forms.ComunicadoFilterForm
    model = models.Comunicado
    template_name = 'comunicados/comunicados_list.html'


class ComunicadoRecibidoListView(ListView):
    form_class = forms.ComunicadoFilterForm
    model = models.Comunicado
    template_name = 'comunicados/comunicados_list.html'

    def get_queryset(self):
        return Comunicado.objects.filter(destinatarios__id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(ComunicadoRecibidoListView, self).get_context_data(**kwargs)
        context['activateViewingButtons'] = True
        return context


class ComunicadoEnviadoListView(ListView):
    form_class = forms.ComunicadoFilterForm
    model = models.Comunicado
    template_name = 'comunicados/comunicados_list.html'

    def get_queryset(self):
        return Comunicado.objects.filter(emisor=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ComunicadoEnviadoListView, self).get_context_data(**kwargs)
        context['activateEditingButtons'] = True
        return context


class ComunicadoCreateView(CreateView):
    model = models.Comunicado
    success_url = reverse_lazy('administracion:comunicados')
    form_class = forms.ComunicadoForm
    template_name = 'comunicados/comunicados_form.html'

    def form_valid(self, form):
        form.instance.emisor = self.request.user
        return super(ComunicadoCreateView, self).form_valid(form)


class ComunicadoDetailView(DetailView):
    model = models.Comunicado
    # success_url = reverse_lazy('administracion:comunicados')
    form_class = forms.ComunicadoForm
    template_name = 'comunicados/comunicados_view.html'

    def form_valid(self, form):
        form.instance.emisor = self.request.user
        return super(ComunicadoDetailView, self).form_valid(form)


class ComunicadoUpdateView(UpdateView):
    model = models.Comunicado
    success_url = reverse_lazy('administracion:comunicados')
    form_class = forms.ComunicadoForm
    template_name = 'comunicados/comunicados_form.html'

    def form_valid(self, form):
        form.instance.emisor = self.request.user
        return super(ComunicadoUpdateView, self).form_valid(form)


class ComunicadoDeleteView(ProtectedDeleteView):
    model = models.Comunicado
    success_url = reverse_lazy('administracion:comunicados')
    template_name = 'comunicados/comunicados_confirm_delete.html'
