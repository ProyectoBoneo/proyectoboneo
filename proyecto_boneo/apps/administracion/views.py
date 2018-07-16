from proyecto_boneo.apps.gutils.django.views import TemplateView


class AdministracionHomeView(TemplateView):
    template_name = 'administracion/home.html'
