# place app url patterns here
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from proyecto_boneo.apps.gutils.django.views import TemplateView

from . import views

app_name = 'eventos'

urlpatterns = [
   url(r'^$', login_required(views.EventosListView.as_view()),
       name='eventos'),

   url(r'^nuevo/$', login_required(views.EventosCreateView.as_view()),
       name='nuevo_evento'),

   url(r'^editar/(?P<pk>\d+)/$', login_required(views.EventosUpdateView.as_view()),
       name='editar_evento'),

   url(r'^eliminar/(?P<pk>\d+)/$', login_required(views.EventosDeleteView.as_view()),
       name='eliminar_evento'),

   url(r'^ayuda/eventos',
       login_required(TemplateView.as_view(template_name='eventos/eventos_ayuda_list.html')),
       name='ayuda_eventos'),

   url(r'^ayuda/nuevo_evento$',
       login_required(TemplateView.as_view(template_name='eventos/eventos_ayuda_nuevo.html')),
       name='ayuda_nuevo_evento'),

   url(r'^ayuda/editar_evento$',
       login_required(TemplateView.as_view(template_name='eventos/eventos_ayuda_editar.html')),
       name='ayuda_editar_evento'),

   url(r'^ayuda/eliminar_evento$',
       login_required(TemplateView.as_view(template_name='eventos/eventos_ayuda_eliminar.html')),
       name='ayuda_eliminar_evento'),

]
