# place app url patterns here
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from proyecto_boneo.apps.administracion.usuarios.decorators import user_is_not_alumno, user_is_alumno, user_is_staff, \
    user_is_profesor, user_is_not_profesor

clases_virtuales_patterns = [
   url(r'^$', user_is_profesor(views.ClaseVirtualListView.as_view()),
       name='clases_virtuales'),

   url(r'^nuevo/$', user_is_profesor(views.ClaseVirtualCreateView.as_view()),
       name='nueva_clase_virtual'),

   url(r'^ver/(?P<pk>\d+)/$', user_is_profesor(views.ClaseVirtualDetailView.as_view()),
        name='ver_clase_virtual'),

   url(r'^editar/(?P<pk>\d+)/$', user_is_profesor(views.ClaseVirtualUpdateView.as_view()),
       name='editar_clase_virtual'),

   url(r'^eliminar/(?P<pk>\d+)/$', user_is_profesor(views.ClaseVirtualDeleteView.as_view()),
       name='eliminar_clase_virtual'),

   url(r'^ingresar/(?P<pk>\d+)/$', login_required(views.ClaseVirtualIngresarDetailView.as_view()),
        name='ingresar_clase_virtual'),

   url(r'^resolver/(?P<pk>\d+)/$', login_required(views.ClaseVirtualResolverEjercicioView.as_view()),
        name='resolver_ejercicio'),

    url(r'^corregir-resultados/(?P<pk>\d+)/$',
        login_required(views.ClaseVirtualCorreccionListView.as_view()),
        name='corregir_resultados_clase_virtual'),

    url(r'^corregir-resultados/(?P<pk>\d+)/alumno/(?P<alumno_pk>\d+)/$',
        login_required(views.ClaseVirtualCorreccionResultadosView.as_view()),
        name='corregir_resultados_clase_virtual'),

    url(r'^resultados/(?P<pk>\d+)/$', login_required(views.ClaseVirtualResultadosView.as_view()),
        name='resultados_clase_virtual')
]


ejercicios_patterns = [
   # url(r'^(?P<claseid>\d+)/ejercicio/nuevo/$', user_is_profesor(views.EjercicioVirtualCreateView.as_view()),
   #     name='nuevo_ejercicio'),

   url(r'^(?P<clase_id>\d+)/ejercicio_texto/nuevo/$', user_is_profesor(views.EjercicioVirtualTextoCreateView.as_view()),
       name='nuevo_ejercicio_texto'),

   url(r'^(?P<clase_id>\d+)/ejercicio_multiple_choice/nuevo/$', user_is_profesor(views.EjercicioVirtualMultipleChoiceCreateView.as_view()),
       name='nuevo_ejercicio_multiple_choice'),

   url(r'^ejercicio_texto/editar/(?P<pk>\d+)/$', user_is_profesor(views.EjercicioVirtualTextoUpdateView.as_view()),
       name='editar_ejercicio_texto'),

   url(r'^ejercicio_multiple_choice/editar/(?P<pk>\d+)/$', user_is_profesor(views.EjercicioVirtualMultipleChoiceUpdateView.as_view()),
       name='editar_ejercicio_multiple_choice'),

   url(r'^ejercicio/eliminar/(?P<pk>\d+)/$', user_is_profesor(views.EjercicioVirtualDeleteView.as_view()),
       name='eliminar_ejercicio')

]

urlpatterns = clases_virtuales_patterns + ejercicios_patterns