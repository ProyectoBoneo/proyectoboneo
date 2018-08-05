from django.conf.urls import url

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from proyecto_boneo.apps.api.perfil_academico.views import PerfilAcademicoAPIView
from proyecto_boneo.apps.api.usuarios.views import UsuarioBoneoView

app_name = 'api'

router = DefaultRouter()

auth_patterns = [
    url(r'^get_token/$', views.obtain_auth_token)
]

view_patterns = [
    url('^perfil_academico/$', PerfilAcademicoAPIView.as_view()),
    url('^usuario/$', UsuarioBoneoView.as_view()),
]

urlpatterns = auth_patterns + view_patterns + router.urls
