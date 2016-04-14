from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from proyecto_boneo.apps.administracion.usuarios.decorators import user_is_not_alumno, user_is_alumno, \
    user_is_profesor_or_staff

urlpatterns = [
    url(r'^materiales/$', user_is_alumno(views.MaterialesFilteredListView.as_view()),
        name='materiales'),

   url(r'^administracion/materiales/$', user_is_not_alumno(views.MaterialesAdminFilteredListView.as_view()),
       name='materiales_admin'),

   url(r'^materiales/materia/([\w-]+)/$', user_is_alumno(views.MaterialesByMateriaFilteredListView.as_view()),
       name='materiales_by_materia'),

   url(r'^$', login_required(views.BibliotecaHomeView.as_view()), name='biblioteca_home'),

   url(r'^administracion/materiales/nuevo/$', user_is_not_alumno(views.MaterialesCreateView.as_view()),
       name='nuevo_material'),

   url(r'^administracion/materiales/editar/(?P<pk>\d+)/$', user_is_not_alumno(views.MaterialesUpdateView.as_view()),
       name='editar_material'),

   url(r'^administracion/materiales/eliminar/(?P<pk>\d+)/$', user_is_profesor_or_staff(views.MaterialesDeleteView.as_view()),
       name='eliminar_material'),

   url(r'^administracion/materiales/ver/(?P<pk>\d+)/$', login_required(views.MaterialesDetailView.as_view()),
       name='ver_material'),

   url(r'^administracion/materiales/buscar/$', login_required(views.MaterialesSearchFilteredListView.as_view()),
       name='buscar_material'),

   # url(r'^administracion/materiales/descargar/(?P<pk>\d+)/$', login_required(views.MaterialesDownloadView.as_view()),
   #     name='descargar_material'),

   url(r'^materiales/solicitar/$', user_is_alumno(views.SolicitudMaterialesCreateView.as_view()),
      name='solicitar_material'),

   url(r'^materiales/ver-solicitudes/$', user_is_alumno(views.SolicitudMaterialesAlumnoFilteredListView.as_view()),
      name='ver_solicitudes'),

   url(r'^materiales/editar-solicitudes/(?P<pk>\d+)/$', user_is_alumno(views.SolicitudMaterialesAlumnoUpdateView.as_view()),
       name='editar_solicitud_material'),

   url(r'^materiales/eliminar-solicitudes/(?P<pk>\d+)/$', user_is_alumno(views.SolicitudMaterialesAlumnoDeleteView.as_view()),
       name='eliminar_solicitud_material'),

   url(r'^materiales/administracion/ver-solicitudes/$', user_is_not_alumno(views.SolicitudMaterialesAdminFilteredListView.as_view()),
      name='ver_solicitudes_admin'),

       url(r'^materiales/administracion/ver-solicitudes-pendientes/$', user_is_not_alumno(views.SolicitudMaterialesPendientesAdminFilteredListView.as_view()),
      name='ver_solicitudes_pendientes_admin'),

   url(r'^materiales/administracion/responder-solicitud/(?P<pk>\d+)/$', user_is_not_alumno(views.ResponderSolicitudMaterialView.as_view()),
       name='responder_solicitud_material_admin'),

   url(r'^materiales/administracion/rechazar-solicitud/(?P<pk>\d+)/$', user_is_not_alumno(views.RechazarSolicitudMaterialView.as_view()),
       name='rechazar_solicitud_material_admin'),

   url(r'^materiales/administracion/eliminar-solicitudes/(?P<pk>\d+)/$', user_is_not_alumno(views.SolicitudMaterialesAdminDeleteView.as_view()),
       name='eliminar_solicitud_material_admin')
]
