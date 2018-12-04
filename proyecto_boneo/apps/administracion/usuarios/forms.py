from django.forms import fields
from django.db.models import Q

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = UsuarioBoneo


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = UsuarioBoneo


class UserGroupsField(fields.Field):
    """
    Form used to convert a list of user groupings into actual users
    """

    def clean(self, value):
        from proyecto_boneo.apps.administracion.alumnos.models import InscripcionAlumno
        from proyecto_boneo.apps.administracion.planes.models import InstanciaCursado
        filters = Q()
        for user_grouping in value:
            destinatario_type, destinatario_id = user_grouping.split('_')
            if destinatario_type == UsuarioBoneo.TYPE_USER:
                filters |= Q(id=destinatario_id)
            elif destinatario_type == UsuarioBoneo.TYPE_DIVISION:
                filters |= Q(alumno__inscripciones__in=InscripcionAlumno.objects.filter(
                    instancia_cursado__in=InstanciaCursado.objects.filter(division_id=destinatario_id)))
            elif destinatario_type == UsuarioBoneo.TYPE_YEAR:
                filters |= Q(alumno__inscripciones__in=InscripcionAlumno.objects.filter(
                    instancia_cursado__in=InstanciaCursado.objects.filter(division__anio=destinatario_id)))
            elif destinatario_type == UsuarioBoneo.TYPE_USER_GROUP:
                if destinatario_id == UsuarioBoneo.USER_GROUP_PROFESORES:
                    filters |= Q(is_profesor=True)
                elif destinatario_id == UsuarioBoneo.USER_GROUP_ALUMNOS:
                    filters |= Q(is_alumno=True)
                elif destinatario_id == UsuarioBoneo.USER_GROUP_ADMIN:
                    filters |= Q(is_staff=True)
        return UsuarioBoneo.objects.filter(filters).distinct().all()
