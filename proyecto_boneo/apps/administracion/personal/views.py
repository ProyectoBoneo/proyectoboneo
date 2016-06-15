from gutils.django.views import CreateView, ProtectedDeleteView, FilteredListView
from django.core.urlresolvers import reverse_lazy

from . import forms, models
from django.views.generic import UpdateView


class PersonaCreateView(CreateView):

    def form_valid(self, form):
        form.instance.crear_usuario(form.cleaned_data['email'])
        return super(PersonaCreateView, self).form_valid(form)


class PersonaUpdateView(UpdateView):

    def form_valid(self, form):
        user_email = form.cleaned_data['email']
        usuario = form.instance.usuario
        usuario.email = user_email
        usuario.username = user_email
        usuario.save()
        return super(PersonaUpdateView, self).form_valid(form)


#region Profesores
class ProfesoresFilteredListView(FilteredListView):
    form_class = forms.ProfesorFilterForm
    model = models.Profesor
    template_name = 'personal/profesores/profesores_list.html'
    
    
class ProfesoresCreateView(PersonaCreateView):
    model = models.Profesor
    success_url = reverse_lazy('administracion:profesores')
    form_class = forms.ProfesorForm
    template_name = 'personal/profesores/profesores_form.html'


class ProfesoresUpdateView(PersonaUpdateView):
    model = models.Profesor
    success_url = reverse_lazy('administracion:profesores')
    form_class = forms.ProfesorForm
    template_name = 'personal/profesores/profesores_form.html'


class ProfesoresDeleteView(ProtectedDeleteView):
    model = models.Profesor
    success_url = reverse_lazy('administracion:profesores')
    template_name = 'personal/profesores/profesores_confirm_delete.html'
#endregion
