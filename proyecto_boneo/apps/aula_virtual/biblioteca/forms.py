from django import forms

from gutils.django.forms import BaseModelForm, BaseFilterForm

from . import models


class MaterialForm(BaseModelForm):

    class Meta:
        model = models.Material
        exclude = []
        labels = {'descripcion': 'Descripción', }

    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if not archivo:
            raise forms.ValidationError('Debe seleccionar un archivo.')
        return archivo


class MaterialFilterForm(BaseFilterForm):
    descripcion = forms.CharField(max_length=100, label='Descripción')

    class Meta:
        filters = {'descripcion': 'descripcion__icontains', }