from django import forms

from . import models

# place form definition here
from gutils.django.forms import BaseModelForm


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


class EncuentroTutoriaForTutoriaForm(BaseModelForm):

    class Meta:
        model = models.EncuentroTutoria
        exclude = ['tutoria']
        labels = {}
