from . import forms, models

# Create your views here.
import datetime
from django.core.urlresolvers import reverse_lazy
from django.forms import formset_factory, model_to_dict
from django.shortcuts import render, redirect
from gutils.django.views import View
from proyecto_boneo.apps.administracion.alumnos.models import Alumno
from proyecto_boneo.apps.administracion.personal.models import Profesor
from proyecto_boneo.apps.administracion.estadias.forms import EstadiaForm
from proyecto_boneo.apps.administracion.usuarios.customViews.views import ListView, CreateView, DetailView, UpdateView, \
    ProtectedDeleteView


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
