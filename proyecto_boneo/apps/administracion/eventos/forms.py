from django.forms import widgets

from proyecto_boneo.apps.gutils.django.forms import BaseModelForm
from proyecto_boneo.apps.administracion.usuarios.forms import UserGroupsField

from . import models


class EventoForm(BaseModelForm):
    participantes = UserGroupsField(required=True, widget=widgets.SelectMultiple)

    class Meta:
        model = models.Evento
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'participantes']
        labels = {
            'descripcion': 'Descripción'
        }
