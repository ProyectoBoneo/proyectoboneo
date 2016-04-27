from proyecto_boneo.apps.administracion.usuarios.customViews.views import TemplateView


class AulaVirtualHomeView(TemplateView):
    template_name = 'aula_virtual/home_administracion.html'

    def get_context_data(self, **kwargs):
        context = super(AulaVirtualHomeView, self).get_context_data(**kwargs)
        context["user"] = self.request.user
        return context
