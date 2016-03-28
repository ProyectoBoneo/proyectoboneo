# place app url patterns here
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from proyecto_boneo.apps.administracion.usuarios.decorators import user_is_not_alumno, user_is_alumno, user_is_staff, \
    user_is_profesor, user_is_not_profesor

estadias_patterns = [
   url(r'^$', user_is_staff(views.EstadiasListView.as_view()),
       name='estadias'),

   url(r'^nuevo/$', user_is_staff(views.EstadiaCreateView.as_view()),
       name='nuevo_estadia'),

  url(r'^ver/(?P<pk>\d+)/$', user_is_staff(views.EstadiaDetailView.as_view()),
       name='ver_estadia'),

   url(r'^editar/(?P<pk>\d+)/$', user_is_staff(views.EstadiaUpdateView.as_view()),
       name='editar_estadia'),

   url(r'^eliminar/(?P<pk>\d+)/$', user_is_staff(views.EstadiaDeleteView.as_view()),
       name='eliminar_estadia')

]

urlpatterns = estadias_patterns