from gutils.django.views import CreateView, UpdateView, ProtectedDeleteView, FilteredListView
from django.core.urlresolvers import reverse_lazy

from . import forms, models


class MaterialesFilteredListView(FilteredListView):
    form_class = forms.MaterialFilterForm
    model = models.Material
    template_name = 'biblioteca_virtual/materiales/materiales_list.html'
    
    
class MaterialesCreateView(CreateView):
    model = models.Material
    success_url = reverse_lazy('materiales')
    form_class = forms.MaterialForm
    template_name = 'biblioteca_virtual/materiales/materiales_form.html'


class MaterialesUpdateView(UpdateView):
    model = models.Material
    success_url = reverse_lazy('materiales')
    form_class = forms.MaterialForm
    template_name = 'biblioteca_virtual/materiales/materiales_form.html'


class MaterialesDeleteView(ProtectedDeleteView):
    model = models.Material
    success_url = reverse_lazy('materiales')
    template_name = 'biblioteca_virtual/materiales/materiales_confirm_delete.html'
