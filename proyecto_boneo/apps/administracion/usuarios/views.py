from django.urls import reverse_lazy
from proyecto_boneo.apps.administracion.usuarios import models
from proyecto_boneo.apps.administracion.usuarios.custom_views.views import DetailView, UpdateView
from proyecto_boneo.apps.administracion.usuarios.forms import CustomUserCreationForm, CustomUserChangeForm


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
