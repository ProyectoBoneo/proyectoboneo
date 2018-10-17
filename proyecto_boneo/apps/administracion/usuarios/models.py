import re

from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from rest_framework.authtoken.models import Token


class UsuarioBoneo(AbstractBaseUser, PermissionsMixin):
    """
    User for the boneo platform
    """
    TYPE_USER = 'usuario'
    TYPE_DIVISION = 'division'
    TYPE_YEAR = 'anio'
    TYPE_USER_GROUP = 'user_group'

    USER_GROUP_ALUMNOS = 'alumnos'
    USER_GROUP_PROFESORES = 'profesores'
    USER_GROUP_ADMIN = 'admin'

    USER_GROUPS = [
        ('Alumnos', USER_GROUP_ALUMNOS),
        ('Profesores', USER_GROUP_PROFESORES),
        ('Administración', USER_GROUP_ADMIN),
    ]

    username = models.CharField(_('username'), max_length=254, unique=True,
                                help_text=_('Required. 254 characters or fewer. Letters, numbers and '
                                            '@/./+/-/_ characters'),
                                validators=[RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'),
                                                           'invalid'), ])
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), max_length=254, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    is_alumno = models.BooleanField(_('alumno'), default=False,
                                    help_text=_('Designates whether this user should be treated as '
                                                'alumno.'))
    is_profesor = models.BooleanField(_('profesor'), default=False,
                                    help_text=_('Designates whether this user should be treated as '
                                                'profesor.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def clean(self):
        for f in ('first_name', 'last_name'):
            cur = getattr(self, f)
            if cur is not None:
                setattr(self, f, cur.strip())

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return u'{} {}'.format(self.first_name, self.last_name).strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    @classmethod
    def build_user_grouping_id(cls, grouping_type, grouping_id):
        """
        Build unique id for the user grouping
        """
        return '{}_{}'.format(grouping_type, grouping_id)

    @classmethod
    def get_user_groupings(cls):
        """
        Build possible user groupings for the platform
        """
        from proyecto_boneo.apps.administracion.planes.models import Division
        possible_destinatarios = []
        possible_destinatarios.extend({'id': cls.build_user_grouping_id(cls.TYPE_USER, user.id),
                                       'text': user.get_full_name(),
                                       'subtext': user.username}
                                      for user in UsuarioBoneo.objects.all())
        possible_destinatarios.extend({'id': cls.build_user_grouping_id(cls.TYPE_DIVISION, division.id),
                                       'text': str(division),
                                       'subtext': 'División'}
                                      for division in Division.objects.filter(activa=True).all())
        possible_destinatarios.extend({'id': cls.build_user_grouping_id(cls.TYPE_YEAR, anio),
                                       'text': '{}º'.format(anio),
                                       'subtext': 'Año de cursado'}
                                      for anio in Division.objects.años_plan())
        possible_destinatarios.extend({
            'id': cls.build_user_grouping_id(cls.TYPE_USER_GROUP, group[1]),
            'text': group[0],
            'subtext': 'Grupo de usuarios'
        } for group in cls.USER_GROUPS)
        return possible_destinatarios

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'auth_user'
        permissions = (("can_view_boneouser", "Can view Boneo User"), )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
