from django import forms

from gutils.django.forms import BaseModelForm, BaseFilterForm

from . import models


class ClaseVirtualForm(BaseModelForm):

    class Meta:
        model = models.ClaseVirtual
        exclude = []
        labels = {}


class EjercicioVirtualForm(BaseModelForm):

    class Meta:
        model = models.EjercicioVirtual
        exclude = ['clase_virtual']
        labels = {}

class EjercicioVirtualTextoForm(BaseModelForm):

    class Meta:
        model = models.ClaseVirtual
        exclude = ['clase_virtual', 'orden_prioridad']
        labels = {}


class EjercicioVirtualMultipleChoice(BaseModelForm):

    class Meta:
        model = models.ClaseVirtual
        exclude = ['clase_virtual', 'orden_prioridad']
        labels = {}


class ClaseVirtualFilterForm(BaseFilterForm):
    descripcion = forms.CharField(max_length=100, label='Descripción')

    class Meta:
        filters = {'descripcion': 'descripcion__icontains', }

