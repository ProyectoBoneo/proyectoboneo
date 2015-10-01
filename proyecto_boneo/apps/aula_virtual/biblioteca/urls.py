from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
   url(r'^materiales/$', login_required(views.MaterialesFilteredListView.as_view()),
       name='materiales'),

   url(r'^materiales/nuevo/$', login_required(views.MaterialesCreateView.as_view()),
       name='nuevo_material'),

   url(r'^materiales/editar/(?P<pk>\d+)/$', login_required(views.MaterialesUpdateView.as_view()),
       name='editar_material'),

   url(r'^materiales/eliminar/(?P<pk>\d+)/$', login_required(views.MaterialesDeleteView.as_view()),
       name='eliminar_material'),
]
