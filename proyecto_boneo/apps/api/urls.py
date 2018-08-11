from django.conf.urls import url

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from proyecto_boneo.apps.api.comunicados.views import ComunicadosViewSet
from proyecto_boneo.apps.api.perfil_academico.views import PerfilAcademicoViewSet, ResultadoEvaluacionViewSet
from proyecto_boneo.apps.api.usuarios.views import UsuarioBoneoView

app_name = 'api'

router = DefaultRouter()

router.register('comunicados', ComunicadosViewSet, base_name='comunicados')
router.register('perfil_academico', PerfilAcademicoViewSet, base_name='perfil_academico')
router.register('resultados_evaluaciones', ResultadoEvaluacionViewSet, base_name='resultados_evaluaciones')

auth_patterns = [
    url(r'^get_token/$', views.obtain_auth_token)
]

view_patterns = [
    url('^usuario/$', UsuarioBoneoView.as_view()),
]

urlpatterns = auth_patterns + view_patterns + router.urls
