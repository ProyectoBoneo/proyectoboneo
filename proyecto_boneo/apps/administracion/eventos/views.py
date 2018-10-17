from django.urls import reverse_lazy
from django.shortcuts import redirect
from proyecto_boneo.apps.administracion.usuarios.custom_views.views import (ListView, CreateView,
                                                                            ProtectedDeleteView, UpdateView)

from proyecto_boneo.apps.administracion.eventos.models import Evento
from . import forms, models


class EventosListView(ListView):
    model = models.Evento
    template_name = 'eventos/eventos_list.html'


class EventosCreateView(CreateView):
    model = models.Evento
    success_url = reverse_lazy('administracion:eventos:eventos')
    form_class = forms.EventoForm
    template_name = 'eventos/eventos_form.html'

    def form_valid(self, form):
        participantes = form.cleaned_data.pop('participantes')
        evento = Evento(**form.cleaned_data)
        evento.save()
        for participante in participantes:
            evento.participantes.add(participante)
        return redirect(self.success_url)


class EventosDeleteView(ProtectedDeleteView):
    model = models.Evento
    success_url = reverse_lazy('administracion:eventos:eventos')
    template_name = 'eventos/eventos_confirm_delete.html'


class EventosUpdateView(UpdateView):
    model = models.Evento
    success_url = reverse_lazy('administracion:eventos:eventos')
    form_class = forms.EventoForm
    template_name = 'eventos/eventos_form.html'
