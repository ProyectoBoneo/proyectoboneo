from django.forms import widgets

from proyecto_boneo.apps.gutils.django.forms import BaseModelForm
from proyecto_boneo.apps.administracion.usuarios.forms import UserGroupsField

from . import models


class ComunicadoForm(BaseModelForm):
    destinatarios = UserGroupsField(required=True, widget=widgets.SelectMultiple)

    class Meta:
        model = models.Comunicado
        exclude = ['emisor']
