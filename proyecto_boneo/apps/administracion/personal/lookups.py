from proyecto_boneo.apps.gutils.django.forms.typeahead.lookups import Lookup, register_lookup

from . import models


class ProfesorLookup(Lookup):
    model = models.Profesor
    search_fields = ['nombre', 'apellido']


register_lookup(ProfesorLookup)
