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
       name='eliminar_clase_virtual')

]

ejercicios_patterns = [
   # url(r'^(?P<claseid>\d+)/ejercicio/nuevo/$', user_is_profesor(views.EjercicioVirtualCreateView.as_view()),
   #     name='nuevo_ejercicio'),

   url(r'^(?P<claseid>\d+)/ejercicio_texto/nuevo/$', user_is_profesor(views.EjercicioVirtualTextoCreateView.as_view()),
       name='nuevo_ejercicio_texto'),

   url(r'^(?P<claseid>\d+)/ejercicio_multiple_choice/nuevo/$', user_is_profesor(views.EjercicioVirtualMultipleChoiceCreateView.as_view()),
       name='nuevo_ejercicio_multiple_choice'),

   url(r'^ejercicio/editar/(?P<pk>\d+)/$', user_is_profesor(views.EjercicioVirtualUpdateView.as_view()),
       name='editar_ejercicio'),

   url(r'^ejercicio/eliminar/(?P<pk>\d+)/$', user_is_profesor(views.EjercicioVirtualDeleteView.as_view()),
       name='eliminar_ejercicio')

]

urlpatterns = clases_virtuales_patterns + ejercicios_patterns