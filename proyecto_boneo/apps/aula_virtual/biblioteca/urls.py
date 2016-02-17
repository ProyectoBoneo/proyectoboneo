from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
   url(r'^materiales/$', login_required(views.MaterialesFilteredListView.as_view()),
       name='materiales'),

   url(r'^administracion/materiales/$', login_required(views.MaterialesFilteredListView.as_view()),
       name='materiales'),

   url(r'^$', login_required(views.BibliotecaHomeView.as_view()), name='biblioteca_home'),

   url(r'^administracion/materiales/nuevo/$', login_required(views.MaterialesCreateView.as_view()),
       name='nuevo_material'),

   url(r'^administracion/materiales/editar/(?P<pk>\d+)/$', login_required(views.MaterialesUpdateView.as_view()),
       name='editar_material'),

   url(r'^administracion/materiales/eliminar/(?P<pk>\d+)/$', login_required(views.MaterialesDeleteView.as_view()),
       name='eliminar_material'),
]
