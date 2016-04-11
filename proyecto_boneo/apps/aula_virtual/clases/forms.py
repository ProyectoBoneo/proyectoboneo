from django import forms
from django.forms import inlineformset_factory, modelformset_factory

from gutils.django.forms import BaseModelForm, BaseFilterForm, BaseForm

from . import models
from proyecto_boneo.apps.aula_virtual.clases.models import EjercicioVirtualMultipleChoice, OpcionEjercicioMultipleChoice


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
        model = models.EjercicioVirtualTexto
        fields = ['ayuda','consigna']
        labels = {}


class EjercicioVirtualMultipleChoiceForm(BaseModelForm):

    class Meta:
        model = models.EjercicioVirtualMultipleChoice
        fields = ['ayuda','pregunta','explicacion']
        labels = {}


class OpcionEjercicioMultipleChoiceForm(BaseModelForm):
    class Meta:
        model = models.OpcionEjercicioMultipleChoice
        fields=['texto','opcion_correcta']
        labels = {}

OpcionEjercicioVirtualFormSet = inlineformset_factory(EjercicioVirtualMultipleChoice, OpcionEjercicioMultipleChoice,
                                                      form=OpcionEjercicioMultipleChoiceForm)
OpcionEjercicioVirtualUpdateFormSet = inlineformset_factory(EjercicioVirtualMultipleChoice, OpcionEjercicioMultipleChoice,
                                                      form=OpcionEjercicioMultipleChoiceForm, extra=0)


class ClaseVirtualFilterForm(BaseFilterForm):
    descripcion = forms.CharField(max_length=100, label='Descripción')

    class Meta:
        filters = {'descripcion': 'descripcion__icontains', }


class TipoEjercicioForm(BaseForm):
    TEXTO = 'texto'
    MULTIPLE_CHOICE = 'multiple_choice'
    TIPO_EJERCICIO_CHOICES = (
        (TEXTO, 'Ejercicio de Texto'),
        (MULTIPLE_CHOICE, 'Ejercicio de Multiple Choice')
    )

    tipo_ejercicio = forms.ChoiceField(
        choices=TIPO_EJERCICIO_CHOICES,
        label="Agregar ejercicio"
    )


class RespuestaEjercicioVirtualTextoForm(BaseModelForm):
    class Meta:
        model = models.RespuestaEjercicioVirtualTexto
        fields=['texto']
        labels = {}


class RespuestaEjercicioVirtualMultipleChoiceForm(BaseModelForm):
    class Meta:
        model = models.RespuestaEjercicioVirtualMultipleChoice
        fields=['opcion_seleccionada']
        labels = {}


class RespuestaEjercicioVirtualCorreccionForm(BaseModelForm):
    class Meta:
        model = models.RespuestaEjercicioVirtual
        fields=['es_correcta', 'id']
        labels = {}
        widgets = {'id': forms.HiddenInput()}

CorregirRespuestaEjercicioVirtualFormSet = modelformset_factory(models.RespuestaEjercicioVirtual,
                                                                form=RespuestaEjercicioVirtualCorreccionForm,
                                                                extra=0)
