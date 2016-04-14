from . import forms, models

from django.core.urlresolvers import reverse_lazy
from gutils.django.views import ListView, CreateView, DetailView, UpdateView, ProtectedDeleteView


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
    success_url = reverse_lazy('administracion:estadias')
    form_class = forms.EstadiaForm
    template_name = 'estadias/estadias_form.html'


class EstadiaUpdateView(UpdateView):
    model = models.Estadia
    success_url = reverse_lazy('administracion:estadias')
    form_class = forms.EstadiaForm
    template_name = 'estadias/estadias_form.html'


class EstadiaDeleteView(ProtectedDeleteView):
    model = models.Estadia
    success_url = reverse_lazy('administracion:estadias')
    template_name = 'estadias/estadias_confirm_delete.html'
