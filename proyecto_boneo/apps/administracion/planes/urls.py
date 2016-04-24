from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from proyecto_boneo.apps.administracion.planes.views.horarios import HorarioPorFechaView, HorarioIrAFechaView
from proyecto_boneo.apps.administracion.usuarios.decorators import user_is_staff

materias_patterns = [
   url(r'^materias/$', user_is_staff(views.MateriasFilteredListView.as_view()),
       name='materias'),

   url(r'^materias/nuevo/$', user_is_staff(views.MateriasCreateView.as_view()),
       name='nueva_materia'),

   url(r'^materias/editar/(?P<pk>\d+)/$', user_is_staff(views.MateriasUpdateView.as_view()),
       name='editar_materia'),

   url(r'^materias/eliminar/(?P<pk>\d+)/$', user_is_staff(views.MateriasDeleteView.as_view()),
       name='eliminar_materia'),

   url(r'^divisiones/profesores_por_materia/$',
       user_is_staff(views.ConfigurarProfesoresMateriasView.as_view()),
       name='configurar_profesores_materias'),

   url(r'^divisiones/(?P<pk>\d+)/horarios_por_materia/$',
       user_is_staff(views.ConfigurarHorariosDivisionView.as_view()),
       name='configurar_horarios_materias'),

   url(r'^horarios/(?P<day>[0-9]+)/(?P<month>[0-9]+)/(?P<year>[0-9]{4})/$',
       HorarioPorFechaView.as_view(),
       name="horario_por_fecha"),

   url(r'^horarios/ir_a_fecha/$',
       HorarioIrAFechaView.as_view(),
       name="ir_a_fecha"),

   url(r'^horarios/hoy/$',
       HorarioPorFechaView.as_view(),
       name="horario_hoy"),
]

plan_patterns = [
   url(r'^divisiones/$', user_is_staff(views.DivisionesListView.as_view()),
       name='divisiones'),

   url(r'^divisiones/configurar/$',
       user_is_staff(views.DivisionesConfigurationView.as_view()),
       name='configurar_divisiones'),

   url(r'^divisiones/generar_instancias_cursado/$',
       user_is_staff(views.DivisionesGenerarInstanciasCursadoView.as_view()),
       name='generar_instancias_cursado'),
]

urlpatterns = materias_patterns + plan_patterns
