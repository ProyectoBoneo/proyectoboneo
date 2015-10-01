from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
   url(r'^profesores/$',
       login_required(views.ProfesoresFilteredListView.as_view()),
       name='profesores'),

   url(r'^profesores/nuevo/$',
       login_required(views.ProfesoresCreateView.as_view()),
       name='nuevo_profesor'),

   url(r'^profesores/editar/(?P<pk>\d+)/$',
       login_required(views.ProfesoresUpdateView.as_view()),
       name='editar_profesor'),

   url(r'^profesores/eliminar/(?P<pk>\d+)/$',
       login_required(views.ProfesoresDeleteView.as_view()),
       name='eliminar_profesor'),
]
