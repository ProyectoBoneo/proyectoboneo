from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^$', login_required(views.AulaVirtualHomeView.as_view()), name='home_administracion'),
    url(r'^biblioteca/', include('proyecto_boneo.apps.aula_virtual.biblioteca.urls')),
    url(r'^clases/', include('proyecto_boneo.apps.aula_virtual.clases.urls'))
]
