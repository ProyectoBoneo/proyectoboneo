from django import forms

from gutils.django.forms import BaseModelForm, BaseFilterForm

from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo

from . import models


class ProfesorFilterForm(BaseFilterForm):
    nombre = forms.CharField(max_length=150, required=False)
    apellido = forms.CharField(max_length=150, required=False)

    class Meta:
        filters = {'nombre': 'nombre__icontains',
                   'apellido': 'apellido__icontains', }


class PersonaForm(BaseModelForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            kwargs['initial'].update({'email': kwargs['instance'].usuario.email})
        super(PersonaForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            current_email = self.instance.usuario.email
        except UsuarioBoneo.DoesNotExist:
            current_email = None

        if email != current_email:
            try:
                UsuarioBoneo.objects.get(email=email)
                raise forms.ValidationError('Este email se encuentra en uso')
            except UsuarioBoneo.DoesNotExist:
                pass
        return email


class ProfesorForm(PersonaForm):

    class Meta:
        model = models.Profesor
        exclude = ['fecha_ingreso', 'legajo', 'usuario']
