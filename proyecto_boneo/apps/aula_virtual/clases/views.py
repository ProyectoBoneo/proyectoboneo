from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.shortcuts import get_object_or_404

from proyecto_boneo.apps.administracion.usuarios.customViews.views import CreateView, UpdateView, ProtectedDeleteView, FilteredListView, ListView, DetailView
from gutils.django.views import View
from django.core.urlresolvers import reverse_lazy

from . import forms, models
from django.views.generic import TemplateView
from proyecto_boneo.apps.aula_virtual.clases.forms import TipoEjercicioForm, OpcionEjercicioVirtualFormSet, \
    RespuestaEjercicioVirtualMultipleChoiceForm, RespuestaEjercicioVirtualTextoForm


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

    def get_context_data(self, **kwargs):
        context = super(ClaseVirtualDetailView, self).get_context_data(**kwargs)
        tipo_ejercicio_form = TipoEjercicioForm()
        context["tipo_ejercicio_form"] = tipo_ejercicio_form
        return context


class ClaseVirtualIngresarDetailView(DetailView):
    model = models.ClaseVirtual
    template_name = 'clase_virtual/clase_virtual_ingresar.html'


# class ClaseVirtualComenzarView(DetailView):
#     def get(self, request, *args, **kwargs):
#         clase_virtual = models.ClaseVirtual.objects.filter(pk=self.kwargs['pk'])
#             # .prefetch_related('ejercicios__respuestas')
#         primer_ejercicio = clase_virtual.first().ejercicios.first()
#         lista_ejercicios = list(clase_virtual.first().ejercicios.all())
#
#         print(lista_ejercicios.index(primer_ejercicio))
#         for ejercicio in lista_ejercicios:
#             if(hasattr(ejercicio,'ejerciciovirtualmultiplechoice')):
#                 print(ejercicio.ejerciciovirtualmultiplechoice.respuestas)
#             elif(hasattr(ejercicio,'ejerciciovirtualtexto')):
#                 print(ejercicio.ejerciciovirtualtexto.respuestas)
#         return;

class ClaseVirtualResolverEjercicioView(View):

     def post(self, request, *args, **kwargs):
        clase_virtual = models.ClaseVirtual.objects.filter(pk=self.kwargs['pk'])
        ejercicio_a_resolver = None
        form_to_render = None
        template_to_render = None
        ejercicio_to_render = None
        tipoPreguntaToRender = None
        if('ejercicioId' in request.POST and 'tipoPregunta' in request.POST):
            form = None
            ejercicio_resuelto = None
            if(request.POST['tipoPregunta'] == 'texto'):
                form = RespuestaEjercicioVirtualTextoForm(request.POST, request.FILES)
                ejercicio_resuelto = models.EjercicioVirtualTexto.objects.filter(id=request.POST['ejercicioId'])
                template_to_render = 'ejercicio_virtual/texto/resolver_ejercicio_virtual_form.html'
                tipoPreguntaToRender = 'texto'
            elif(request.POST['tipoPregunta'] == 'multiple_choice'):
                template_to_render = 'ejercicio_virtual/multiple_choice/resolver_ejercicio_virtual_form.html'
                tipoPreguntaToRender = 'multiple_choice'
                form = RespuestaEjercicioVirtualMultipleChoiceForm(request.POST, request.FILES)
                ejercicio_resuelto = models.EjercicioVirtualMultipleChoice.objects.filter(id=request.POST['ejercicioId'])
            if form.is_valid():
                try:
                    form.instance.alumno = self.request.user.alumno
                except :
                    form.instance.alumno = models.Alumno.objects.first()
                form.instance.ejercicio = ejercicio_resuelto.first()
                nueva_respuesta = form.save()
                id_list = list(clase_virtual.first().ejercicios.values_list('id', flat=True))
                try:
                    next_id = id_list[id_list.index(ejercicio_resuelto.first().ejerciciovirtual_ptr_id) + 1]
                    ejercicio_a_resolver = models.EjercicioVirtual.objects.get(id=next_id)
                except IndexError:
                    pass
            else:
                return render(request, template_to_render, {
                                            'form':form_to_render,
                                            'ejercicio': ejercicio_resuelto.first(),
                                            'tipoPregunta': tipoPreguntaToRender,
                                            'user': self.request.user
                                            } )
        else:
            ejercicio_a_resolver = clase_virtual.first().ejercicios.first()
        if(ejercicio_a_resolver.is_ejercicio_virtual_multiple_choice()):
            form_to_render = RespuestaEjercicioVirtualMultipleChoiceForm()
            template_to_render = 'ejercicio_virtual/multiple_choice/resolver_ejercicio_virtual_form.html'
            ejercicio_to_render = ejercicio_a_resolver.ejercicio_instance()
            tipoPreguntaToRender = 'multiple_choice'
        elif(ejercicio_a_resolver.is_ejercicio_virtual_texto()):
            form_to_render = RespuestaEjercicioVirtualTextoForm()
            template_to_render = 'ejercicio_virtual/texto/resolver_ejercicio_virtual_form.html'
            ejercicio_to_render = ejercicio_a_resolver.ejercicio_instance()
            tipoPreguntaToRender = 'texto'
        return render(request, template_to_render, {
                                            'form':form_to_render,
                                            'ejercicio': ejercicio_to_render,
                                            'tipoPregunta': tipoPreguntaToRender,
                                            'user': self.request.user
                                            } )



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


class EjercicioVirtualTextoCreateView(CreateView):
    model = models.EjercicioVirtualTexto
    form_class = forms.EjercicioVirtualTextoForm
    template_name = 'ejercicio_virtual/texto/ejercicio_virtual_form.html'

    def form_valid(self, form):
        clase_virtual = models.ClaseVirtual.objects.get(pk=self.kwargs['claseid'])
        form.instance.clase_virtual = clase_virtual
        return super(EjercicioVirtualTextoCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('aula_virtual:ver_clase_virtual', kwargs={'pk': self.object.clase_virtual.id})


class EjercicioVirtualMultipleChoiceCreateView(CreateView):
    model = models.EjercicioVirtualMultipleChoice
    form_class = forms.EjercicioVirtualMultipleChoiceForm
    template_name = 'ejercicio_virtual/multiple_choice/ejercicio_virtual_form.html'

    # def form_valid(self, form):
    #     clase_virtual = models.ClaseVirtual.objects.get(pk=self.kwargs['claseid'])
    #     form.instance.clase_virtual = clase_virtual
    #     return super(EjercicioVirtualMultipleChoiceCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('aula_virtual:ver_clase_virtual', kwargs={'pk': self.object.clase_virtual.id})

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        opcion_formset = OpcionEjercicioVirtualFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  opcion_formset=opcion_formset))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        opcion_formset = OpcionEjercicioVirtualFormSet(self.request.POST)
        if (form.is_valid() and opcion_formset.is_valid()):
            return self.form_valid(form, opcion_formset)
        else:
            return self.form_invalid(form, opcion_formset)

    def form_valid(self, form, opcion_formset):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        clase_virtual = models.ClaseVirtual.objects.get(pk=self.kwargs['claseid'])
        form.instance.clase_virtual = clase_virtual
        self.object = form.save()
        opcion_formset.instance = self.object
        opcion_formset.save()
        return HttpResponseRedirect(self.get_success_url())
        # return super(EjercicioVirtualMultipleChoiceCreateView, self).form_valid(form)

    def form_invalid(self, form, opcion_formset):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  opcion_formset=opcion_formset))

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