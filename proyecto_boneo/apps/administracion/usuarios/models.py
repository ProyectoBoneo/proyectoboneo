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

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'auth_user'
        permissions = (("can_view_boneouser", "Can view Boneo User"), )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
