# place app url patterns here
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from proyecto_boneo.apps.administracion.usuarios.decorators import user_is_not_alumno, user_is_alumno, user_is_staff, \
    user_is_profesor, user_is_not_profesor

tutorias_patterns = [
   url(r'^$', login_required(views.TutoriasListView.as_view()),
       name='tutorias'),

   url(r'^nuevo/$', user_is_staff(views.TutoriaCreateView.as_view()),
       name='nuevo_tutoria'),

  url(r'^ver/(?P<pk>\d+)/$', login_required(views.TutoriaDetailView.as_view()),
       name='ver_tutoria'),

   url(r'^editar/(?P<pk>\d+)/$', user_is_staff(views.TutoriaUpdateView.as_view()),
       name='editar_tutoria'),

   url(r'^eliminar/(?P<pk>\d+)/$', user_is_staff(views.TutoriaDeleteView.as_view()),
       name='eliminar_tutoria')
]

encuentrotutorias_patterns = [
   url(r'^encuentro/$', login_required(views.EncuentroTutoriasListView.as_view()),
       name='encuentrotutorias'),

   url(r'^encuentro/nuevo/$', login_required(views.EncuentroTutoriaCreateView.as_view()),
       name='nuevo_encuentrotutoria'),

  url(r'^encuentro/ver/(?P<pk>\d+)/$', login_required(views.EncuentroTutoriaDetailView.as_view()),
       name='ver_encuentrotutoria'),

   url(r'^encuentro/editar/(?P<pk>\d+)/$', login_required(views.EncuentroTutoriaUpdateView.as_view()),
       name='editar_encuentrotutoria'),

   url(r'^encuentro/eliminar/(?P<pk>\d+)/$', login_required(views.EncuentroTutoriaDeleteView.as_view()),
       name='eliminar_encuentrotutoria')
]

urlpatterns = tutorias_patterns + encuentrotutorias_patterns