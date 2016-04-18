from django import forms
from django.forms.formsets import formset_factory

from gutils.django.forms import BaseModelForm, BaseFilterForm, BaseFormsetForm, BaseForm
from gutils.django.forms.typeahead.widgets import TypeaheadDropDownModelWidget

from . import models
from proyecto_boneo.apps.administracion.personal.models import Profesor
from proyecto_boneo.apps.administracion.personal.lookups import ProfesorLookup
from proyecto_boneo.apps.administracion.planes.models import Materia


class MateriaForm(BaseModelForm):

    class Meta:
        model = models.Materia
        labels = {'descripcion': 'Descripción',
                  'anio': 'Año del plan'}
        exclude = []
        widgets = {'anio': forms.Select()}

    def __init__(self, *args, **kwargs):
        super(MateriaForm, self).__init__(*args, **kwargs)
        años_posibles = models.Division.objects.filter(
            activa=True).order_by('anio').values('anio').distinct()
        choices = [(str(año['anio']), año['anio']) for año in años_posibles]
        self.fields['anio'].widget.choices = choices


class MateriaFilterForm(BaseFilterForm):
    descripcion = forms.CharField(max_length=150, required=False, label='Descripción')

    class Meta:
        filters = {'descripcion': 'descripcion__icontains', }


AÑOS_CHOICES = [(str(i), i) for i in range(1, 11)]


class ConfigurarCantidadAniosForm(BaseForm):
    cantidad_anios = forms.IntegerField(widget=forms.Select(choices=AÑOS_CHOICES),
                                        label='Años del plan')


class ConfigurarCantidadDivisionesForm(BaseFormsetForm):
    anio = forms.IntegerField()
    cantidad_divisiones = forms.IntegerField(widget=forms.Select(choices=AÑOS_CHOICES),
                                             label='Cantidad de divisiones')


CantidadDivisionesFormset = formset_factory(ConfigurarCantidadDivisionesForm,
                                            can_delete=True, extra=0)


class ConfigurarProfesoresMateriasForm(BaseFormsetForm):
    instancia_cursado = forms.ModelChoiceField(queryset=models.InstanciaCursado.objects.all())
    profesor = forms.ModelChoiceField(queryset=Profesor.objects.all(), empty_label=None,
                                      widget=TypeaheadDropDownModelWidget(ProfesorLookup),
                                      required=False)


ConfigurarMateriasProfesoresFormset = formset_factory(ConfigurarProfesoresMateriasForm,
                                                      can_delete=True, extra=0)


class ConfigurarHorariosMateriasForm(BaseFormsetForm):
    id = forms.IntegerField(required= False)
    dia_semana = forms.IntegerField(widget=forms.Select(choices=
                                    models.Horario.objects.get_dias_semana_choices()),
                                    label='Dia semana',
                                    required=False
                                    )
    materia = forms.ModelChoiceField(queryset=Materia.objects.all(), empty_label=None,
                                      required=False)
    hora_inicio = forms.TimeField(required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Hora Inicio'}))
    hora_fin = forms.TimeField(required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Hora Fin'}))

    def __init__(self, *args, **kwargs):
        super(ConfigurarHorariosMateriasForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs['hidden'] = 'hidden'


ConfigurarMateriasHorariosFormset = formset_factory(ConfigurarHorariosMateriasForm,
                                                      can_delete=True, extra=0)
