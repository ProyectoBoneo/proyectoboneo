from django import forms
from django.forms import inlineformset_factory, modelformset_factory

from proyecto_boneo.apps.gutils.django.forms import BaseModelForm, BaseFilterForm, BaseForm

from . import models
from proyecto_boneo.apps.aula_virtual.clases.models import EjercicioVirtual,OpcionEjercicio


class ClaseVirtualForm(BaseModelForm):
    def __init__(self, profesor, *args, **kwargs):
        super(ClaseVirtualForm, self).__init__(*args, **kwargs)
        self.fields['materia'].queryset = models.Materia.objects.filter(
            instancias_cursado__profesor_titular=profesor).distinct()

    class Meta:
        model = models.ClaseVirtual
        exclude = []


class EjercicioVirtualTextoForm(BaseModelForm):

    class Meta:
        model = models.EjercicioVirtual
        fields = ['ayuda', 'puntaje','consigna']


class EjercicioVirtualMultipleChoiceForm(BaseModelForm):

    class Meta:
        model = models.EjercicioVirtual
        fields = ['ayuda', 'puntaje','consigna', 'explicacion']


class OpcionEjercicioMultipleChoiceForm(BaseModelForm):
    class Meta:
        model = models.OpcionEjercicio
        fields = ['texto','opcion_correcta']

OpcionEjercicioVirtualFormSet = inlineformset_factory(EjercicioVirtual, OpcionEjercicio,
                                                      form=OpcionEjercicioMultipleChoiceForm)
OpcionEjercicioVirtualUpdateFormSet = inlineformset_factory(EjercicioVirtual,
                                                            OpcionEjercicio,
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
        model = models.RespuestaEjercicioVirtual
        fields = ['texto']


class RespuestaEjercicioVirtualMultipleChoiceForm(BaseModelForm):
    class Meta:
        model = models.RespuestaEjercicioVirtual
        fields = ['opcion_seleccionada']


class RespuestaEjercicioVirtualCorreccionForm(BaseModelForm):
    class Meta:
        model = models.RespuestaEjercicioVirtual
        fields = ['puntaje_obtenido', 'id', 'observaciones']
        labels = {}
        widgets = {'id': forms.HiddenInput()}

CorregirRespuestaEjercicioVirtualFormSet = modelformset_factory(models.RespuestaEjercicioVirtual,
                                                                form=RespuestaEjercicioVirtualCorreccionForm,
                                                                extra=0)


class CorregirEvaluacionEscritaForm(BaseForm):
    nota = forms.FloatField(label='Nota', min_value=1, max_value=10)
