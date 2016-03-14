from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    url(r'^materiales/$', login_required(views.MaterialesFilteredListView.as_view()),
        name='materiales'),

   url(r'^administracion/materiales/$', login_required(views.MaterialesAdminFilteredListView.as_view()),
       name='materiales_admin'),

   url(r'^materiales/materia/([\w-]+)/$', login_required(views.MaterialesByMateriaFilteredListView.as_view()),
       name='materiales_by_materia'),

   url(r'^$', login_required(views.BibliotecaHomeView.as_view()), name='biblioteca_home'),

   url(r'^administracion/materiales/nuevo/$', login_required(views.MaterialesCreateView.as_view()),
       name='nuevo_material'),

   url(r'^administracion/materiales/editar/(?P<pk>\d+)/$', login_required(views.MaterialesUpdateView.as_view()),
       name='editar_material'),

   url(r'^administracion/materiales/eliminar/(?P<pk>\d+)/$', login_required(views.MaterialesDeleteView.as_view()),
       name='eliminar_material'),

   url(r'^administracion/materiales/ver/(?P<pk>\d+)/$', login_required(views.MaterialesDetailView.as_view()),
       name='ver_material'),

   url(r'^administracion/materiales/buscar/$', login_required(views.MaterialesSearchFilteredListView.as_view()),
       name='buscar_material'),

   # url(r'^administracion/materiales/descargar/(?P<pk>\d+)/$', login_required(views.MaterialesDownloadView.as_view()),
   #     name='descargar_material'),

   url(r'^materiales/solicitar/$', login_required(views.SolicitudMaterialesCreateView.as_view()),
      name='solicitar_material'),

   url(r'^materiales/ver-solicitudes/$', login_required(views.SolicitudMaterialesAlumnoFilteredListView.as_view()),
      name='ver_solicitudes'),

   url(r'^materiales/editar-solicitudes/(?P<pk>\d+)/$', login_required(views.SolicitudMaterialesAlumnoUpdateView.as_view()),
       name='editar_solicitud_material'),

   url(r'^materiales/eliminar-solicitudes/(?P<pk>\d+)/$', login_required(views.SolicitudMaterialesAlumnoDeleteView.as_view()),
       name='eliminar_solicitud_material'),

   url(r'^materiales/administracion/ver-solicitudes/$', login_required(views.SolicitudMaterialesAdminFilteredListView.as_view()),
      name='ver_solicitudes_admin'),

   url(r'^materiales/administracion/responder-solicitud/(?P<pk>\d+)/$', login_required(views.ResponderSolicitudMaterialView.as_view()),
       name='responder_solicitud_material_admin'),

   url(r'^materiales/administracion/rechazar-solicitud/(?P<pk>\d+)/$', login_required(views.RechazarSolicitudMaterialView.as_view()),
       name='rechazar_solicitud_material_admin'),

   url(r'^materiales/administracion/eliminar-solicitudes/(?P<pk>\d+)/$', login_required(views.SolicitudMaterialesAdminDeleteView.as_view()),
       name='eliminar_solicitud_material_admin')
]
