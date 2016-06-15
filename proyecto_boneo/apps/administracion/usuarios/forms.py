from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = UsuarioBoneo
        # fields = UserCreationForm.Meta.fields + ('',)


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = UsuarioBoneo
        # fields = UserCreationForm.Meta.fields + ('',)

