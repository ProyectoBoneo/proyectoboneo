from django import forms

from . import models

# place form definition here
from proyecto_boneo.apps.gutils.django.forms import BaseModelForm
from proyecto_boneo.apps.gutils.django.forms.typeahead.widgets import TypeaheadDropDownModelWidget
from proyecto_boneo.apps.administracion.alumnos.lookups import AlumnoLookup
from proyecto_boneo.apps.administracion.alumnos.lookups import ResponsableSearchLookup


class EstadiaForm(BaseModelForm):

    class Meta:
        model = models.Estadia
        exclude = []
        labels = {}
        widgets = {'responsable': TypeaheadDropDownModelWidget(ResponsableSearchLookup),
           'alumno': TypeaheadDropDownModelWidget(AlumnoLookup)}
        # widgets = {'destinatarios': forms.CheckboxSelectMultiple}
