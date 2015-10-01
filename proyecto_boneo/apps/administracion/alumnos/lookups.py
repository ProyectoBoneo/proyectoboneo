from gutils.django.forms.typeahead.lookups import Lookup, register_lookup

from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo

from . import models
from .forms import ResponsableForm


class ResponsableLookup(Lookup):
    model = models.Responsable
    form_class = ResponsableForm

    @classmethod
    def save_model(cls, form):
        user_email = form.cleaned_data['email']
        user = UsuarioBoneo(username=user_email,
                            email=user_email)
        user.save()
        form.instance.usuario = user
        return super(ResponsableLookup, cls).save_model(form)

register_lookup(ResponsableLookup)
