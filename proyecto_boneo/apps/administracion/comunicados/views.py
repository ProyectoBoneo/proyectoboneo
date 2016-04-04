from gutils.django.views import CreateView, UpdateView, ProtectedDeleteView, ListView, DetailView
from django.core.urlresolvers import reverse_lazy

from . import forms, models

from proyecto_boneo.apps.administracion.comunicados.models import Comunicado


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
    form_class = forms.ComunicadoForm
    template_name = 'comunicados/comunicados_view.html'

    def form_valid(self, form):
        form.instance.emisor = self.request.user
        return super(ComunicadoCreateView, self).form_valid(form)


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
