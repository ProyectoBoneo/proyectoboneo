from gutils.django.views import TemplateView


class AulaVirtualHomeView(TemplateView):
    template_name = 'aula_virtual/home.html'
