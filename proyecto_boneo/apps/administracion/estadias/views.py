from . import forms, models

from django.urls import reverse_lazy
from proyecto_boneo.apps.gutils.django.views import ListView, CreateView, DetailView, UpdateView, ProtectedDeleteView, TemplateView


class EstadiasListView(ListView):
    model = models.Estadia
    template_name = 'estadias/estadias_list.html'


class EstadiasResponsableListView(ListView):
    model = models.Estadia
    template_name = 'estadias/estadias_list.html'

    def get_queryset(self):
        return models.Estadia.objects.filter(usuario=self.request.user)


class EstadiaDetailView(DetailView):
    model = models.Estadia
    template_name = 'estadias/estadias_view.html'

class EstadiaCreateView(CreateView):
    model = models.Estadia
    success_url = reverse_lazy('administracion:estadias:estadias')
    form_class = forms.EstadiaForm
    template_name = 'estadias/estadias_form.html'


class EstadiaUpdateView(UpdateView):
    model = models.Estadia
    success_url = reverse_lazy('administracion:estadias:estadias')
    form_class = forms.EstadiaForm
    template_name = 'estadias/estadias_form.html'


class EstadiaDeleteView(ProtectedDeleteView):
    model = models.Estadia
    success_url = reverse_lazy('administracion:estadias:estadias')
    template_name = 'estadias/estadias_confirm_delete.html'


class EstadiaAyudaTemplateView(TemplateView):
    template_name = 'estadias/estadias_ayuda_list.html'

class EstadiaAyudaNuevoTemplateView(TemplateView):
    template_name = 'estadias/estadias_ayuda_nuevo.html'

class EstadiaAyudaEditarTemplateView(TemplateView):
    template_name = 'estadias/estadias_ayuda_editar.html'

class EstadiaAyudaEliminarTemplateView(TemplateView):
    template_name = 'estadias/estadias_ayuda_eliminar.html'
