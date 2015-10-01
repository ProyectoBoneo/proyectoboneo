from gutils.django.views import TemplateView

from django.core.urlresolvers import reverse
from django.shortcuts import redirect


def home_redirect_router(request, *args, **kwargs):
    if request.user.is_staff:
        return HomeView.as_view()(request, *args, **kwargs)
    else:
        return redirect(reverse('aula_virtual:home'))
    pass


class HomeView(TemplateView):
    template_name = 'home/home.html'
