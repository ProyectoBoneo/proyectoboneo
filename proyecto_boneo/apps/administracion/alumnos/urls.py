from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = patterns('',
                       #region alumnos
                       url(r'^$', login_required(views.AlumnosFilteredListView.as_view()),
                           name='alumnos'),

                       url(r'^nuevo/$', login_required(views.AlumnosCreateView.as_view()),
                           name='nuevo_alumno'),

                       url(r'^(?P<pk>\d+)/editar/$',
                           login_required(views.AlumnosUpdateView.as_view()),
                           name='editar_alumno'),

                       url(r'^(?P<pk>\d+)/eliminar/$',
                           login_required(views.AlumnosDeleteView.as_view()),
                           name='eliminar_alumno'),

                       url(r'^(?P<pk>\d+)/inscripciones/$',
                           login_required(views.AlumnosInscripcionesView.as_view()),
                           name='inscripciones_alumno'),
                       #endregion

                       #region responsables
                       url(r'^responsables/$',
                           login_required(views.ResponsablesFilteredListView.as_view()),
                           name='responsables'),

                       url(r'^responsables/nuevo/$',
                           login_required(views.ResponsablesCreateView.as_view()),
                           name='nuevo_responsable'),

                       url(r'^responsables/(?P<pk>\d+)/editar/$',
                           login_required(views.ResponsablesUpdateView.as_view()),
                           name='editar_responsable'),

                       url(r'^responsables/(?P<pk>\d+)/eliminar/$',
                           login_required(views.ResponsablesDeleteView.as_view()),
                           name='eliminar_responsable'),
                       #endregion
                       )
