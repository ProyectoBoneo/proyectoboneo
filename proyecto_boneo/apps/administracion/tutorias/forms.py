from django import forms

from . import models

# place form definition here
from django.forms import ModelForm, NumberInput
from gutils.django.forms import BaseModelForm
from gutils.django.forms.typeahead.widgets import TypeaheadDropDownModelWidget
from proyecto_boneo.apps.administracion.alumnos.lookups import AlumnoLookup
from proyecto_boneo.apps.administracion.personal.lookups import ProfesorLookup


class TimeInput(forms.TextInput):
    input_type = 'time'


class TutoriaForm(ModelForm):

    class Meta:
        model = models.Tutoria
        exclude = []
        labels = {'anio': 'Año'}
        widgets = {'profesor': TypeaheadDropDownModelWidget(ProfesorLookup),
                   'alumno': TypeaheadDropDownModelWidget(AlumnoLookup),
                   'anio': NumberInput(attrs={'class':'form-control'})}


class EncuentroTutoriaForm(BaseModelForm):

    class Meta:
        model = models.EncuentroTutoria
        exclude = []
        labels = {}
        widgets = {
            'hora' : TimeInput()
        }

class EncuentroTutoriaForTutoriaForm(BaseModelForm):

    class Meta:
        model = models.EncuentroTutoria
        exclude = ['tutoria']
        labels = {}
