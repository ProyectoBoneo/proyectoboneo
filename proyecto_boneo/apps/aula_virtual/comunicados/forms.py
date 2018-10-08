from django.db.models import Q
from django.forms import fields, widgets

from proyecto_boneo.apps.gutils.django.forms import BaseModelForm
from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo
from proyecto_boneo.apps.administracion.alumnos.models import InscripcionAlumno
from proyecto_boneo.apps.administracion.planes.models import InstanciaCursado
from proyecto_boneo.apps.aula_virtual.comunicados.models import DestinatarioComunicado

from . import models


class DestinatariosField(fields.Field):
    def clean(self, value):
        filters = Q()
        for destinatario in value:
            destinatario_type, destinatario_id = destinatario.split('_')
            if destinatario_type == DestinatarioComunicado.TYPE_USER:
                filters |= Q(id=destinatario_id)
            elif destinatario_type == DestinatarioComunicado.TYPE_DIVISION:
                filters |= Q(alumno__inscripciones__in=InscripcionAlumno.objects.filter(
                    instancia_cursado__in=InstanciaCursado.objects.filter(division_id=destinatario_id)))
            elif destinatario_type == DestinatarioComunicado.TYPE_YEAR:
                filters |= Q(alumno__inscripciones__in=InscripcionAlumno.objects.filter(
                    instancia_cursado__in=InstanciaCursado.objects.filter(anio_cursado=destinatario_id)))
            elif destinatario_type == DestinatarioComunicado.TYPE_USER_GROUP:
                if destinatario_id == DestinatarioComunicado.USER_GROUP_PROFESORES:
                    filters |= Q(is_profesor=True)
                elif destinatario_id == DestinatarioComunicado.USER_GROUP_ALUMNOS:
                    filters |= Q(is_alumno=True)
                elif destinatario_id == DestinatarioComunicado.USER_GROUP_ADMIN:
                    filters |= Q(is_staff=True)
        return UsuarioBoneo.objects.filter(filters).distinct().all()


class ComunicadoForm(BaseModelForm):
    destinatarios = DestinatariosField(required=True, widget=widgets.SelectMultiple)

    class Meta:
        model = models.Comunicado
        exclude = ['emisor']
