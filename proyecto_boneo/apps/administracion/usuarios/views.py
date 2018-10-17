import json

from django.urls import reverse_lazy
from django.shortcuts import HttpResponse
from django.views.generic import View
from proyecto_boneo.apps.administracion.usuarios import models
from proyecto_boneo.apps.administracion.usuarios.custom_views.views import DetailView, UpdateView
from proyecto_boneo.apps.administracion.usuarios.forms import CustomUserCreationForm, CustomUserChangeForm
from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo


class UsuarioDetailView(DetailView):
    model = models.UsuarioBoneo
    form_class = CustomUserCreationForm
    template_name = 'usuarios/usuarios_view.html'

    def get_object(self, **kwargs):
        return models.UsuarioBoneo.objects.get(pk=self.request.user.pk)


class UsuarioUpdateView(UpdateView):
    model = models.UsuarioBoneo
    success_url = reverse_lazy('administracion:usuarios:usuarios')
    form_class = CustomUserChangeForm
    template_name = 'usuarios/usuarios_form.html'

    def get_object(self, **kwargs):
        return models.UsuarioBoneo.objects.get(pk=self.request.user.pk)


class UserGroupingsView(View):
    """
    This view will retrieve user groupings filtered by a search term
    """

    def get(self, request, *args, **kwargs):
        user_groupings = UsuarioBoneo.get_user_groupings()
        search_term = request.GET['term'].lower()
        return HttpResponse(json.dumps({'results': [grouping for grouping in user_groupings
                            if search_term in grouping['text'].lower() or
                            search_term in grouping['subtext'].lower()]}))
