from django.shortcuts import render, redirect
from proyecto_boneo.apps.administracion.usuarios.customViews.views import CreateView, UpdateView, ProtectedDeleteView, \
    TemplateView, DetailView, ListView, FilteredListView
from gutils.django.views import View
from django.core.urlresolvers import reverse_lazy

from . import forms, models
from proyecto_boneo.apps.administracion.planes.models import Materia
from collections import defaultdict
from proyecto_boneo.apps.aula_virtual.biblioteca.forms import MaterialForm, SolicitudMaterialRechazoForm


def get_materias_grouped_by_anio():
    result = defaultdict(list)
    materias = Materia.objects.all()
    for materia in materias:
        result[materia.anio].append(materia)
    result_dict = dict(result)
    print(result_dict)
    return result_dict


class MaterialesFilteredListView(FilteredListView):
    form_class = forms.MaterialFilterForm
    model = models.Material
    template_name = 'biblioteca_virtual/materiales/materiales_list.html'

    def get_context_data(self, **kwargs):
        context = super(MaterialesFilteredListView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class MaterialesSearchFilteredListView(FilteredListView):
    form_class = forms.MaterialSearchFilterForm
    model = models.Material
    template_name = 'biblioteca_virtual/materiales/materiales_search.html'

    def get_context_data(self, **kwargs):
        context = super(MaterialesSearchFilteredListView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class MaterialesAdminFilteredListView(FilteredListView):
    form_class = forms.MaterialFilterForm
    model = models.Material
    template_name = 'biblioteca_virtual/materiales/administracion/materiales_list.html'

    def get_context_data(self, **kwargs):
        context = super(MaterialesAdminFilteredListView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


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
    queryset = models.Material.objects.all()

    def get_context_data(self, **kwargs):
        context = super(BibliotecaHomeView, self).get_context_data(**kwargs)
        context['materia_list'] = Materia.objects.all()
        context['materia_dict'] = get_materias_grouped_by_anio()
        # context['pinned_material_list'] = models.Material.objects.filter(materialAlumno__marked_as_pinned=True).filter(
        #     materialAlumno_usuario__username=self.request.user)
        return context


# TODO: ADD Form Mixin to display a filter like filteredListViews
class MaterialesByMateriaFilteredListView(ListView):
    form_class = forms.MaterialFilterForm
    template_name = 'biblioteca_virtual/materiales/materiales_list.html'

    def get_queryset(self):
        # self._filter_queryset(self.request)
        self.materia = Materia.objects.get(pk=self.args[0])
        return models.Material.objects.filter(materia=self.materia)

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
        rechazo_solicitud_form = SolicitudMaterialRechazoForm(instance = solicitud_material)
        return render(request, self.template_name, {'solicitud_material': solicitud_material,
                                                    'form':form,
                                                    'rechazo_solicitud_form': rechazo_solicitud_form,
                                                    'user': self.request.user
                                                    } )

    def post(self, request, *args, **kwargs):
        form = MaterialForm(request.POST, request.FILES)
        solicitud_material = models.SolicitudMaterial.objects.get(pk=self.kwargs['pk'])
        # check whether it's valid:
        if form.is_valid():
            nuevo_material = form.save()
            solicitud_material.material = nuevo_material
            solicitud_material.aceptada = True
            solicitud_material.pendiente_de_respuesta = False
            solicitud_material.save()
            return redirect(reverse_lazy('aula_virtual:materiales_admin'))
        else:
            rechazo_solicitud_form = SolicitudMaterialRechazoForm(instance = solicitud_material)
            return render(request, self.template_name, {'solicitud_material': solicitud_material,
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
        # self._filter_queryset(self.request)
        # self.usuario = models.UsuarioBoneo.objects.get(pk=self.request.user)
        return models.SolicitudMaterial.objects.filter(pendiente_de_respuesta=True)


class SolicitudMaterialesAdminFilteredListView(FilteredListView):
    form_class = forms.SolicitudMaterialFilterForm
    model = models.SolicitudMaterial
    template_name = 'biblioteca_virtual/solicitud_materiales/administracion/solicitud_materiales_list.html'

    def get_context_data(self, **kwargs):
        context = super(SolicitudMaterialesAdminFilteredListView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
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