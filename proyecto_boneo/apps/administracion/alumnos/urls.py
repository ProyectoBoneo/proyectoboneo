from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from . import views
from proyecto_boneo.apps.administracion.usuarios.decorators import user_is_staff

urlpatterns = patterns('',
                       #region alumnos
                       url(r'^$', user_is_staff(views.AlumnosFilteredListView.as_view()),
                           name='alumnos'),

                       url(r'^nuevo/$', user_is_staff(views.AlumnosCreateView.as_view()),
                           name='nuevo_alumno'),

                       url(r'^(?P<pk>\d+)/editar/$',
                           user_is_staff(views.AlumnosUpdateView.as_view()),
                           name='editar_alumno'),

                       url(r'^(?P<pk>\d+)/eliminar/$',
                           user_is_staff(views.AlumnosDeleteView.as_view()),
                           name='eliminar_alumno'),

                       url(r'^(?P<pk>\d+)/inscripciones/$',
                           user_is_staff(views.AlumnosInscripcionesView.as_view()),
                           name='inscripciones_alumno'),
                       #endregion

                       #region responsables
                       url(r'^responsables/$',
                           user_is_staff(views.ResponsablesFilteredListView.as_view()),
                           name='responsables'),

                       url(r'^responsables/nuevo/$',
                           user_is_staff(views.ResponsablesCreateView.as_view()),
                           name='nuevo_responsable'),

                       url(r'^responsables/(?P<pk>\d+)/editar/$',
                           user_is_staff(views.ResponsablesUpdateView.as_view()),
                           name='editar_responsable'),

                       url(r'^responsables/(?P<pk>\d+)/eliminar/$',
                           user_is_staff(views.ResponsablesDeleteView.as_view()),
                           name='eliminar_responsable'),
                       #endregion
                       )
