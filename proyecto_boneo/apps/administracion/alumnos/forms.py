from django import forms
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from gutils.django.forms import BaseFilterForm, BaseFormsetModelForm, BaseForm, BaseFormsetForm
from gutils.django.forms.typeahead.widgets import TypeaheadDropDownAddModelWidget

from proyecto_boneo.apps.administracion.personal.forms import PersonaForm
from proyecto_boneo.apps.administracion.alumnos.models import InscripcionAlumno, Alumno

from . import models
from proyecto_boneo.apps.administracion.planes.models import InstanciaCursado, Horario


class ResponsableForm(PersonaForm):

    class Meta:
        model = models.Responsable
        exclude = ['fecha_ingreso', 'usuario']


class AlumnoFilterForm(BaseFilterForm):
    nombre = forms.CharField(max_length=150, required=False)
    apellido = forms.CharField(max_length=150, required=False)

    class Meta:
        filters = {'nombre': 'nombre__icontains',
                   'apellido': 'apellido__icontains', }


class ResponsableFilterForm(BaseFilterForm):
    nombre = forms.CharField(max_length=150, required=False)
    apellido = forms.CharField(max_length=150, required=False)

    class Meta:
        filters = {'nombre': 'nombre__icontains',
                   'apellido': 'apellido__icontains', }


from . import lookups


class AlumnoForm(PersonaForm):

    class Meta:
        model = models.Alumno
        widgets = {'responsable': TypeaheadDropDownAddModelWidget(lookups.ResponsableLookup)}
        exclude = ['fecha_ingreso', 'legajo', 'usuario']


class InscripcionForm(BaseFormsetModelForm):

    class Meta:
        model = InscripcionAlumno
        fields = ['instancia_cursado', ]

InscripcionesFormset = modelformset_factory(InscripcionAlumno,
                                            form=InscripcionForm,
                                            can_delete=True,
                                            extra=1)


class AsistenciaForm(BaseFormsetForm):
    id = forms.IntegerField(required=False)
    alumno_id = forms.IntegerField()
    asistio = forms.BooleanField(initial=False, required=False)


AsistenciaFormset = formset_factory(AsistenciaForm,
                                can_delete=False, extra=0)
