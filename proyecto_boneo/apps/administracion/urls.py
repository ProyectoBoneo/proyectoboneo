from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'administracion'

urlpatterns = [
    url(r'^$', login_required(views.AdministracionHomeView.as_view()), name='home'),
    url(r'^alumnos/', include('proyecto_boneo.apps.administracion.alumnos.urls')),
    url(r'^personal/', include('proyecto_boneo.apps.administracion.personal.urls')),
    url(r'^planes/', include('proyecto_boneo.apps.administracion.planes.urls')),
    url(r'^tutorias/', include('proyecto_boneo.apps.administracion.tutorias.urls')),
    url(r'^estadias/', include('proyecto_boneo.apps.administracion.estadias.urls')),
    url(r'^usuarios/', include('proyecto_boneo.apps.administracion.usuarios.urls')),
    url(r'^eventos/', include('proyecto_boneo.apps.administracion.eventos.urls')),
]
