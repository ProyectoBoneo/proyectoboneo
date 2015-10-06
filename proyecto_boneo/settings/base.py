import os
from django.conf import global_settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '_x3usyf+o)be7x033m_61@fft1lk88-amr^=4#_vz$(-i6vsbv'

DEBUG = True

TEMPLATE_DEBUG = True

DATE_FORMAT = 'd/m/Y'

DATETIME_FORMAT = 'd/m/Y H:i'

DATETIME_INPUT_FORMATS = (
    '%d/%m/%Y %H:%M',
)

DATE_INPUT_FORMATS = (
    '%d/%m/%Y',
)

# Application definition

DJANGO_APPS = ('django.contrib.admin',
               'django.contrib.auth',
               'django.contrib.contenttypes',
               'django.contrib.sessions',
               'django.contrib.messages',
               'django.contrib.staticfiles',)

THIRD_PARTY_APPS = ('django_extensions', )

PROJECT_APPS = ('gutils',
                'gutils.django.forms.typeahead',
                'gutils.django.apps.utils',
                'proyecto_boneo.apps.administracion.alumnos',
                'proyecto_boneo.apps.administracion.personal',
                'proyecto_boneo.apps.administracion.planes',
                'proyecto_boneo.apps.administracion.usuarios',
                'proyecto_boneo.apps.aula_virtual.biblioteca',
                'proyecto_boneo.apps.aula_virtual.clases',
                )

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'gutils.django.middleware.ThreadLocalMiddleware',
)

ROOT_URLCONF = 'proyecto_boneo.urls'

WSGI_APPLICATION = 'proyecto_boneo.wsgi.application'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'proyecto_boneo',
        'USER': 'boneo',
        'PASSWORD': 'boneo',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ]
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-AR'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True

APPEND_SLASH = True

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

LOGIN_URL = '/login/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)

AUTH_USER_MODEL = 'usuarios.UsuarioBoneo'

