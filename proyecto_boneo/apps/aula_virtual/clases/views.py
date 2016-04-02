from django.shortcuts import render

from django.shortcuts import get_object_or_404
from gutils.django.views import CreateView, UpdateView, ProtectedDeleteView, FilteredListView, ListView, DetailView, \
    View
from django.core.urlresolvers import reverse_lazy

from . import forms, models
from django.views.generic import TemplateView


class ClaseVirtualListView(ListView):
    form_class = forms.ClaseVirtualFilterForm
    model = models.ClaseVirtual
    template_name = 'clase_virtual/clase_virtual_list.html'


class ClaseVirtualCreateView(CreateView):
    model = models.ClaseVirtual
    form_class = forms.ClaseVirtualForm
    template_name = 'clase_virtual/clase_virtual_form.html'

    def get_success_url(self):
        return reverse_lazy('aula_virtual:ver_clase_virtual', kwargs={'pk': self.object.id})


class ClaseVirtualDetailView(DetailView):
    model = models.ClaseVirtual
    form_class = forms.ClaseVirtualForm
    template_name = 'clase_virtual/clase_virtual_view.html'


class ClaseVirtualUpdateView(UpdateView):
    model = models.ClaseVirtual
    form_class = forms.ClaseVirtualForm
    template_name = 'clase_virtual/clase_virtual_form.html'

    def get_success_url(self):
        return reverse_lazy('aula_virtual:ver_clase_virtual', kwargs={'pk': self.object.id})


class ClaseVirtualDeleteView(ProtectedDeleteView):
    model = models.ClaseVirtual
    success_url = reverse_lazy('aula_virtual:clase_virtual')
    template_name = 'clase_virtual/clase_virtual_confirm_delete.html'

# TODO: Para manejar los tipos de ejercicio posiblemente se mas facil hacerlo heredando de view
# e implementando get y post
class EjercicioVirtualCreateView(CreateView):
    model = models.EjercicioVirtual
    form_class = forms.EjercicioVirtualForm
    template_name = 'ejercicio_virtual/ejercicio_virtual_form.html'

    def form_valid(self, form):
        clase_virtual = models.ClaseVirtual.objects.get(pk=self.kwargs['claseid'])
        form.instance.clase_virtual = clase_virtual
        return super(EjercicioVirtualCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('aula_virtual:ver_clase_virtual', kwargs={'pk': self.object.clase_virtual.id})


class EjercicioVirtualUpdateView(UpdateView):
    model = models.EjercicioVirtual
    form_class = forms.EjercicioVirtualForm
    template_name = 'ejercicio_virtual/ejercicio_virtual_form.html'

    def get_success_url(self):
        return reverse_lazy('aula_virtual:ver_clase_virtual', kwargs={'pk': self.object.clase_virtual.id})


class EjercicioVirtualDeleteView(ProtectedDeleteView):
    model = models.EjercicioVirtual
    template_name = 'ejercicio_virtual/ejercicio_virtual_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('aula_virtual:ver_clase_virtual', kwargs={'pk': self.object.clase_virtual.id})