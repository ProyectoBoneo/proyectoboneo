from django import forms

from . import models

# place form definition here
from gutils.django.forms import BaseModelForm

class TimeInput(forms.TextInput):
    input_type = 'time'


class TutoriaForm(BaseModelForm):

    class Meta:
        model = models.Tutoria
        exclude = []
        labels = {}


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
