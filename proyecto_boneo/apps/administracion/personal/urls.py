from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from proyecto_boneo.apps.administracion.usuarios.decorators import user_is_staff

app_name = 'personal'

urlpatterns = [
   url(r'^profesores/$',
       user_is_staff(views.ProfesoresFilteredListView.as_view()),
       name='profesores'),

   url(r'^profesores/nuevo/$',
       user_is_staff(views.ProfesoresCreateView.as_view()),
       name='nuevo_profesor'),

   url(r'^profesores/editar/(?P<pk>\d+)/$',
       user_is_staff(views.ProfesoresUpdateView.as_view()),
       name='editar_profesor'),

   url(r'^profesores/eliminar/(?P<pk>\d+)/$',
       user_is_staff(views.ProfesoresDeleteView.as_view()),
       name='eliminar_profesor'),

   url(r'^ayuda/profesor$',
       login_required(views.ProfesoresAyudaTemplateView.as_view()),
       name='ayuda_profesores'),

   url(r'^ayuda/nuevo_profesor$',
       login_required(views.ProfesoresAyudaNuevoTemplateView.as_view()),
       name='ayuda_nuevo_profesor'),

   url(r'^ayuda/editar_profesor$',
       login_required(views.ProfesoresAyudaEditarTemplateView.as_view()),
       name='ayuda_editar_profesor'),

   url(r'^ayuda/eliminar_profesor$',
       login_required(views.ProfesoresAyudaEliminarTemplateView.as_view()),
       name='ayuda_eliminar_profesor'),
]
