from django import forms
from proyecto_boneo.apps.gutils.django.forms import BaseModelForm, BaseFilterForm

from . import models


class ComunicadoForm(BaseModelForm):

    class Meta:
        model = models.Comunicado
        exclude = ['emisor']
