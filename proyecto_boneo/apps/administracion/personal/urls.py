from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from proyecto_boneo.apps.administracion.usuarios.decorators import user_is_staff

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
]
