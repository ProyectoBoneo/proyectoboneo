from django import forms
from gutils.django.forms import BaseModelForm, BaseFilterForm

from . import models


class ComunicadoForm(BaseModelForm):

    class Meta:
        model = models.Comunicado
        exclude = ['emisor']


class ComunicadoFilterForm(BaseFilterForm):
    descripcion = forms.CharField(max_length=100, label='Descripción')

    class Meta:
        filters = {'descripcion': 'descripcion__icontains', }
