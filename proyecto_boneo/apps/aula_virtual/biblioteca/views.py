from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy

from . import forms, models
from django.views.generic import View
from proyecto_boneo.apps.administracion.planes.models import Materia
from collections import defaultdict
from proyecto_boneo.apps.administracion.usuarios.customViews.views import CreateView, UpdateView, ProtectedDeleteView, \
    DetailView, ListView, FilteredListView, TemplateView
from proyecto_boneo.apps.aula_virtual.biblioteca.forms import MaterialForm, SolicitudMaterialRechazoForm


def get_materias_grouped_by_anio():
    result = defaultdict(list)
    materias = Materia.objects.all()
    for materia in materias:
        result[materia.anio].append(materia)
    return dict(result)


class MaterialesFilteredListView(FilteredListView):
    form_class = forms.MaterialFilterForm
    model = models.Material
    template_name = 'biblioteca_virtual/materiales/materiales_list.html'

    def get_queryset(self):
        return models.Material.objects.publicados()


class MaterialesSearchFilteredListView(FilteredListView):
    form_class = forms.MaterialSearchFilterForm
    queryset = models.Material
    template_name = 'biblioteca_virtual/materiales/materiales_search.html'

    def get_base_queryset(self):
        return models.Material.objects.publicados()


class MaterialesAdminFilteredListView(FilteredListView):
    form_class = forms.MaterialFilterForm
    model = models.Material
    template_name = 'biblioteca_virtual/materiales/administracion/materiales_list.html'


class MaterialesCreateView(CreateView):
    model = models.Material
    success_url = reverse_lazy('aula_virtual:materiales_admin')
    form_class = forms.MaterialForm
    template_name = 'biblioteca_virtual/materiales/administracion/materiales_form.html'


class MaterialesUpdateView(UpdateView):
    model = models.Material
    success_url = reverse_lazy('aula_virtual:materiales_admin')
    form_class = forms.MaterialForm
    template_name = 'biblioteca_virtual/materiales/administracion/materiales_form.html'


class MaterialesDeleteView(ProtectedDeleteView):
    model = models.Material
    success_url = reverse_lazy('aula_virtual:materiales_admin')
    template_name = 'biblioteca_virtual/materiales/administracion/materiales_confirm_delete.html'


class MaterialesDetailView(DetailView):
    model = models.Material
    template_name = 'biblioteca_virtual/materiales/materiales_view.html'

    def get_context_data(self, **kwargs):
            context = super(MaterialesDetailView, self).get_context_data(**kwargs)
            if(self.request.user.is_alumno):
                context['current_materia'] = self.object.materia
                context['materia_dict'] = get_materias_grouped_by_anio()
            return context


class BibliotecaHomeView(ListView):
    form_class = forms.MaterialFilterForm
    context_object_name = 'material_list'
    template_name = 'biblioteca_virtual/administracion/home.html'
    model = models.Material

    def get_queryset(self):
        return models.Material.objects.publicados()

    def get_context_data(self, **kwargs):
        context = super(BibliotecaHomeView, self).get_context_data(**kwargs)
        context['materia_list'] = Materia.objects.all()
        context['materia_dict'] = get_materias_grouped_by_anio()
        return context


class MaterialesByMateriaFilteredListView(ListView):
    form_class = forms.MaterialFilterForm
    template_name = 'biblioteca_virtual/materiales/materiales_list.html'
    model = Materia

    def get_queryset(self):
        self.materia = Materia.objects.get(pk=self.args[0])
        return models.Material.objects.publicados().filter(materia=self.materia)

    def get_context_data(self, **kwargs):
        context = super(MaterialesByMateriaFilteredListView, self).get_context_data(**kwargs)
        context['current_materia'] = self.materia
        context['materia_dict'] = get_materias_grouped_by_anio()
        return context


class ResponderSolicitudMaterialView(View):
    template_name = 'biblioteca_virtual/solicitud_materiales/administracion/solicitud_materiales_form.html'

    def get(self, request, *args, **kwargs):
        form = MaterialForm()
        solicitud_material = models.SolicitudMaterial.objects.get(pk=self.kwargs['pk'])
        rechazo_solicitud_form = SolicitudMaterialRechazoForm(instance=solicitud_material)
        return render(request, self.template_name, {'solicitud_material': solicitud_material,
                                                    'form':form,
                                                    'rechazo_solicitud_form': rechazo_solicitud_form,
                                                    'user': self.request.user
                                                    })

    def post(self, request, *args, **kwargs):
        form = MaterialForm(request.POST, request.FILES)
        solicitud_material = models.SolicitudMaterial.objects.get(pk=self.kwargs['pk'])
        if form.is_valid():
            nuevo_material = form.save()
            solicitud_material.material = nuevo_material
            solicitud_material.aceptada = True
            solicitud_material.pendiente_de_respuesta = False
            solicitud_material.save()
            return redirect(reverse_lazy('aula_virtual:materiales_admin'))
        else:
            rechazo_solicitud_form = SolicitudMaterialRechazoForm(instance = solicitud_material)
            return render(request, self.template_name, {
                        'solicitud_material': solicitud_material,
                        'form':form,
                        'rechazo_solicitud_form': rechazo_solicitud_form,
                        'user': self.request.user
                        } )


class RechazarSolicitudMaterialView(View):
    def post(self, request , *args, **kwargs):
        solicitud_material = models.SolicitudMaterial.objects.get(pk=self.kwargs['pk'])
        rechazo_solicitud_form = SolicitudMaterialRechazoForm(request.POST ,instance=solicitud_material)
        if rechazo_solicitud_form.is_valid():
            solicitud_material = rechazo_solicitud_form.save(commit=False)
            solicitud_material.aceptada = False
            solicitud_material.pendiente_de_respuesta = False
            solicitud_material.save()
            return redirect(reverse_lazy('aula_virtual:materiales_admin'))


class SolicitudMaterialesCreateView(CreateView):
    model = models.SolicitudMaterial
    success_url = reverse_lazy('aula_virtual:ver_solicitudes')
    form_class = forms.SolicitudMaterialForm
    template_name = 'biblioteca_virtual/solicitud_materiales/solicitud_materiales_form.html'

    def form_valid(self, form):
        form.instance.solicitante = self.request.user
        return super(SolicitudMaterialesCreateView, self).form_valid(form)


class SolicitudMaterialesAdminUpdateView(UpdateView):
    model = models.SolicitudMaterial
    success_url = reverse_lazy('aula_virtual:biblioteca_home')
    form_class = forms.SolicitudMaterialForm
    template_name = 'biblioteca_virtual/solicitud_materiales/administracion/solicitud_materiales_form.html'

    def form_valid(self, form):
        form.instance.solicitante = self.request.user
        return super(SolicitudMaterialesAdminUpdateView, self).form_valid(form)


class SolicitudMaterialesAdminDeleteView(ProtectedDeleteView):
    model = models.SolicitudMaterial
    success_url = reverse_lazy('aula_virtual:biblioteca_home')
    template_name = 'biblioteca_virtual/solicitud_materiales/administracion/solicitud_materiales_confirm_delete.html'


class SolicitudMaterialesPendientesAdminFilteredListView(ListView):
    form_class = forms.SolicitudMaterialFilterForm
    model = models.SolicitudMaterial
    template_name = 'biblioteca_virtual/solicitud_materiales/administracion/solicitud_materiales_pendientes_list.html'

    def get_queryset(self):
        return models.SolicitudMaterial.objects.filter(pendiente_de_respuesta=True)


class SolicitudMaterialesAdminFilteredListView(FilteredListView):
    form_class = forms.SolicitudMaterialFilterForm
    model = models.SolicitudMaterial
    template_name = 'biblioteca_virtual/solicitud_materiales/administracion/solicitud_materiales_list.html'

    def get_context_data(self, **kwargs):
        context = super(SolicitudMaterialesAdminFilteredListView, self).get_context_data(**kwargs)
        return context


class SolicitudMaterialesAlumnoFilteredListView(ListView):
    form_class = forms.SolicitudMaterialFilterForm
    model = models.SolicitudMaterial
    template_name = 'biblioteca_virtual/solicitud_materiales/solicitud_materiales_list.html'

    def get_queryset(self):
        return models.SolicitudMaterial.objects.filter(solicitante=self.request.user)


class SolicitudMaterialesAlumnoUpdateView(UpdateView):
    model = models.SolicitudMaterial
    success_url = reverse_lazy('aula_virtual:ver_solicitudes')
    form_class = forms.SolicitudMaterialForm
    template_name = 'biblioteca_virtual/solicitud_materiales/solicitud_materiales_form.html'

    def form_valid(self, form):
        form.instance.solicitante = self.request.user
        return super(SolicitudMaterialesAlumnoUpdateView, self).form_valid(form)


class SolicitudMaterialesAlumnoDeleteView(ProtectedDeleteView):
    model = models.SolicitudMaterial
    success_url = reverse_lazy('aula_virtual:ver_solicitudes')
    template_name = 'biblioteca_virtual/solicitud_materiales/solicitud_materiales_confirm_delete.html'


class MaterialesAyudaTemplateView(TemplateView):
    template_name = 'biblioteca_virtual/materiales/materiales_ayuda_list.html'

class MaterialesAyudaNuevoTemplateView(TemplateView):
    template_name = 'biblioteca_virtual/materiales/materiales_ayuda_nuevo.html'

class MaterialesAyudaEditarTemplateView(TemplateView):
    template_name = 'biblioteca_virtual/materiales/materiales_ayuda_editar.html'

class MaterialesAyudaEliminarTemplateView(TemplateView):
    template_name = 'biblioteca_virtual/materiales/materiales_ayuda_eliminar.html'

class MaterialesAyudaBuscarTemplateView(TemplateView):
    template_name = 'biblioteca_virtual/materiales/materiales_ayuda_buscar.html'

class MaterialesAyudaVerTemplateView(TemplateView):
    template_name = 'biblioteca_virtual/materiales/materiales_ayuda_ver.html'

class SolicitudMaterialesAyudaTemplateView(TemplateView):
    template_name = 'biblioteca_virtual/solicitud_materiales/solicitud_materiales_ayuda_list.html'

class SolicitudMaterialesAyudaPendientesTemplateView(TemplateView):
    template_name = 'biblioteca_virtual/solicitud_materiales/solicitud_materiales_ayuda_pendiente_list.html'

class SolicitudMaterialesAyudaNuevoTemplateView(TemplateView):
    template_name = 'biblioteca_virtual/solicitud_materiales/solicitud_materiales_ayuda_nuevo.html'

class SolicitudMaterialesAyudaEditarTemplateView(TemplateView):
    template_name = 'biblioteca_virtual/solicitud_materiales/solicitud_materiales_ayuda_editar.html'

class SolicitudMaterialesAyudaEliminarTemplateView(TemplateView):
    template_name = 'biblioteca_virtual/solicitud_materiales/solicitud_materiales_ayuda_eliminar.html'
