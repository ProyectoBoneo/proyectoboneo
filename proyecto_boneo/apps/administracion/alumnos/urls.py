from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from proyecto_boneo.apps.administracion.usuarios.decorators import user_is_staff

app_name = 'alumnos'

urlpatterns = [
    # region alumnos
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

    url(r'^ayuda/alumno$',
        login_required(views.AlumnosAyudaTemplateView.as_view()),
        name='ayuda_alumnos'),

    url(r'^ayuda/nuevo_alumno$',
        login_required(views.AlumnosAyudaNuevoTemplateView.as_view()),
        name='ayuda_nuevo_alumno'),

    url(r'^ayuda/editar_alumno$',
        login_required(views.AlumnosAyudaEditarTemplateView.as_view()),
        name='ayuda_editar_alumno'),

    url(r'^ayuda/eliminar_alumno$',
        login_required(views.AlumnosAyudaEliminarTemplateView.as_view()),
        name='ayuda_eliminar_alumno'),

    url(r'^ayuda/inscripciones_alumno$',
        login_required(views.AlumnosAyudaInscripcionesTemplateView.as_view()),
        name='ayuda_inscripciones_alumno'),
    # endregion

    # region responsables
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

    url(r'^ayuda/responsable$',
        login_required(views.ResponsablesAyudaTemplateView.as_view()),
        name='ayuda_responsables'),

    url(r'^ayuda/nuevo_responsable$',
        login_required(views.ResponsablesAyudaNuevoTemplateView.as_view()),
        name='ayuda_nuevo_responsable'),

    url(r'^ayuda/editar_responsable$',
        login_required(views.ResponsablesAyudaEditarTemplateView.as_view()),
        name='ayuda_editar_responsable'),

    url(r'^ayuda/eliminar_responsable$',
        login_required(views.ResponsablesAyudaEliminarTemplateView.as_view()),
        name='ayuda_eliminar_responsable'),
    # endregion

    # region asistencia
    url(r'asistencia/(?P<pk>\d+)/(?P<day>[0-9]+)/(?P<month>[0-9]+)/(?P<year>[0-9]{4})/',
        views.AsistenciaView.as_view(),
        name='asistencia')
    # endregion
]
