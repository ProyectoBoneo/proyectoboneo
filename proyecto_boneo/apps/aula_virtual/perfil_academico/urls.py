from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
   url(r'^estado_academico/(?P<alumno_pk>\d+)/$', login_required(views.EstadoAcademicoView.as_view()),
       name='estado_academico'),
   url(r'^estado_academico/(?P<alumno_pk>\d+)/imprimir/$', login_required(views.EstadoAcademicoReportView.as_view()),
       name='estado_academico_report'),
]

