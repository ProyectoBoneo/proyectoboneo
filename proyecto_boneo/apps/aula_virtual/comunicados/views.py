import datetime

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render
from gutils.django.views import CreateView, ListView, DetailView

from proyecto_boneo.apps.aula_virtual.comunicados.models import Comunicado, DestinatarioComunicado
from . import forms, models


class ComunicadoRecibidoListView(ListView):
    form_class = forms.ComunicadoFilterForm
    model = models.Comunicado
    template_name = 'comunicados/comunicados_list.html'

    def get_queryset(self):
        return Comunicado.objects.filter(destinatarios__id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(ComunicadoRecibidoListView, self).get_context_data(**kwargs)
        context['title'] = 'Comunicados recibidos'
        return context


class ComunicadoEnviadoListView(ListView):
    form_class = forms.ComunicadoFilterForm
    model = models.Comunicado
    template_name = 'comunicados/comunicados_list.html'

    def get_queryset(self):
        return Comunicado.objects.filter(emisor=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ComunicadoEnviadoListView, self).get_context_data(**kwargs)
        context['title'] = 'Comunicados enviados'
        return context


class ComunicadoCreateView(CreateView):
    model = models.Comunicado
    success_url = reverse_lazy('aula_virtual:comunicados_recibidos')
    form_class = forms.ComunicadoForm
    template_name = 'comunicados/comunicados_form.html'

    def form_valid(self, form):
        form.instance.emisor = self.request.user
        comunicado = Comunicado(emisor=self.request.user, mensaje=form.cleaned_data['mensaje'])
        comunicado.save()
        for destinatario in form.cleaned_data['destinatarios']:
            DestinatarioComunicado.objects.create(destinatario=destinatario,
                                                  comunicado=comunicado)
        return redirect(self.success_url)


class ComunicadoDetailView(DetailView):
    model = models.Comunicado
    form_class = forms.ComunicadoForm
    template_name = 'comunicados/comunicados_view.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return render(request, self.template_name, context)

    def get_object(self, queryset=None):
        comunicado = super(ComunicadoDetailView, self).get_object()

        try:
            destinatario = DestinatarioComunicado.objects.get(destinatario=self.request.user,
                                                              comunicado=comunicado)
            destinatario.fecha_leido = datetime.datetime.now()
            destinatario.save()
        except DestinatarioComunicado.DoesNotExist:
            pass
        return comunicado
