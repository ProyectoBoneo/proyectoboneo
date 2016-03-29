from django import forms

from . import models

# place form definition here
from gutils.django.forms import BaseModelForm


class EstadiaForm(BaseModelForm):

    class Meta:
        model = models.Estadia
        exclude = []
        labels = {}
        # widgets = {'destinatarios': forms.CheckboxSelectMultiple}