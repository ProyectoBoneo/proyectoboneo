from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from proyecto_boneo.apps.administracion.usuarios import views

app_name = 'usuarios'

urlpatterns = [
    url(r'^ver/$', login_required(views.UsuarioDetailView.as_view()),
        name='mi_perfil'),
    url(r'^editar/$', login_required(views.UsuarioUpdateView.as_view()),
        name='editar_mi_perfil'),
    url(r'^grupos_usuarios/$', login_required(views.UserGroupingsView.as_view()),
        name='grupos_usuarios'),
]
