from proyecto_boneo.settings.base import *

DEBUG = False
TEMPLATE_DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'proyectoboneo',
        'USER': 'proyectoboneo',
        'PASSWORD': 'proyectoboneo',
        'HOST': 'proyecto-boneo.cvttgl8gstqj.us-west-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = ['ec2-52-40-113-106.us-west-2.compute.amazonaws.com', '127.0.0.1', 'localhost']
