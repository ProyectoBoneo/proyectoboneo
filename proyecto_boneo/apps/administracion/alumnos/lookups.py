from proyecto_boneo.apps.gutils.django.forms.typeahead.lookups import Lookup, register_lookup
from proyecto_boneo.apps.administracion.personal.forms import PersonaForm

from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo

from . import models

class ResponsableForm(PersonaForm):

    class Meta:
        model = models.Responsable
        exclude = ['fecha_ingreso', 'usuario']

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


class AlumnoLookup(Lookup):
    model = models.Alumno
    search_fields = ['nombre', 'apellido']

register_lookup(AlumnoLookup)


class ResponsableSearchLookup(Lookup):
    model = models.Responsable
    search_fields = ['nombre', 'apellido']

register_lookup(ResponsableSearchLookup)
