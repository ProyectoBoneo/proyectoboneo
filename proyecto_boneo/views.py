from gutils.django.views import TemplateView

from django.core.urlresolvers import reverse
from django.shortcuts import redirect


def home_redirect_router(request, *args, **kwargs):
    if request.user.is_staff:
        return StaffHomeView.as_view()(request, *args, **kwargs)
    elif request.user.is_alumno:
        return AlumnoHomeView.as_view()(request, *args, **kwargs)
    elif request.user.is_profesor:
        return ProfesorHomeView.as_view()(request, *args, **kwargs)
    else:
        return redirect(reverse('aula_virtual:home'))
    pass


class StaffHomeView(TemplateView):
    template_name = 'home/home.html'

class AlumnoHomeView(TemplateView):
    template_name = 'home/alumno_home.html'

class ProfesorHomeView(TemplateView):
     template_name = 'home/profesor_home.html'