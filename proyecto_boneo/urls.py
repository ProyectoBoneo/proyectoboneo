from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from gutils.django.forms.typeahead.views import TypeaheadAddModelView, TypeaheadView

from .views import home_redirect_router

typeahead_patterns = [
    url(r'^typeahead/$', TypeaheadView.as_view(), name='typeahead'),
    url(r'^typeahead-add/(?P<lookup_name>\w+)$', TypeaheadAddModelView.as_view(),
        name='typeahead-add'),
]

auth_patterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^password_change/$', auth_views.password_change, name='password_change'),
    url(r'^password_change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]

project_patterns = [
    url(r'^$', login_required(home_redirect_router), name='home'),
    url(r'administracion/', include('proyecto_boneo.apps.administracion.urls',
                                    namespace='administracion')),
    url(r'aula_virtual/', include('proyecto_boneo.apps.aula_virtual.urls', namespace='aula_virtual'))
]

urlpatterns = auth_patterns + typeahead_patterns + project_patterns
