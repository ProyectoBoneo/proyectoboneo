from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

materias_patterns = [
   url(r'^materias/$', login_required(views.MateriasFilteredListView.as_view()),
       name='materias'),

   url(r'^materias/nuevo/$', login_required(views.MateriasCreateView.as_view()),
       name='nueva_materia'),

   url(r'^materias/editar/(?P<pk>\d+)/$', login_required(views.MateriasUpdateView.as_view()),
       name='editar_materia'),

   url(r'^materias/eliminar/(?P<pk>\d+)/$', login_required(views.MateriasDeleteView.as_view()),
       name='eliminar_materia'),

   url(r'^divisiones/profesores_por_materia/$',
       login_required(views.ConfigurarProfesoresMateriasView.as_view()),
       name='configurar_profesores_materias'),
]

plan_patterns = [
   url(r'^divisiones/$', login_required(views.DivisionesListView.as_view()),
       name='divisiones'),

   url(r'^divisiones/configurar/$',
       login_required(views.DivisionesConfigurationView.as_view()),
       name='configurar_divisiones'),

   url(r'^divisiones/generar_instancias_cursado/$',
       login_required(views.DivisionesGenerarInstanciasCursadoView.as_view()),
       name='generar_instancias_cursado'),
]

urlpatterns = materias_patterns + plan_patterns
