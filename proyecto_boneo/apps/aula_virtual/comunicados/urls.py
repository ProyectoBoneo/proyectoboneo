from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
   url(r'^recibidos/$', login_required(views.ComunicadoRecibidoListView.as_view()),
       name='comunicados_recibidos'),

   url(r'^enviados/$', login_required(views.ComunicadoEnviadoListView.as_view()),
       name='comunicados_enviados'),

   url(r'^nuevo/$', login_required(views.ComunicadoCreateView.as_view()),
       name='nuevo_comunicado'),

   url(r'^ver/(?P<pk>\d+)/$', login_required(views.ComunicadoDetailView.as_view()),
       name='ver_comunicado'),
]

