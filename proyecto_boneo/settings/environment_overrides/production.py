from proyecto_boneo.settings.base import *

DEBUG = False
TEMPLATE_DEBUG = False
DATABASES = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'proyectoboneo',
    'USER': 'proyectoboneo',
    'PASSWORD': 'proyectoboneo',
    'HOST': 'proyecto-boneo.cvttgl8gstqj.us-west-2.rds.amazonaws.com',
    'PORT': '5432',
}
