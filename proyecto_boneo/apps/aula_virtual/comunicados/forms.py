from django import forms
from gutils.django.forms import BaseModelForm, BaseFilterForm

from . import models


class ComunicadoForm(BaseModelForm):

    class Meta:
        model = models.Comunicado
        exclude = ['emisor']
