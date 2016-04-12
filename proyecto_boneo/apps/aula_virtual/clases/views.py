from django.db.models import Count, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from proyecto_boneo.apps.administracion.personal.models import Profesor

from proyecto_boneo.apps.administracion.usuarios.customViews.views import CreateView, UpdateView, ProtectedDeleteView, FilteredListView, ListView, DetailView
from gutils.django.views import View
from django.core.urlresolvers import reverse_lazy

from . import forms, models
from proyecto_boneo.apps.aula_virtual.clases.forms import TipoEjercicioForm, OpcionEjercicioVirtualFormSet, \
    RespuestaEjercicioVirtualMultipleChoiceForm, RespuestaEjercicioVirtualTextoForm, \
    CorregirRespuestaEjercicioVirtualFormSet, OpcionEjercicioVirtualUpdateFormSet


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

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ClaseVirtualCreateView, self).get_form_kwargs(**kwargs)
        kwargs['profesor'] = self.request.user.profesor
        return kwargs


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


class ClaseVirtualResultadosView(View):
    template_name = 'clase_virtual/clase_virtual_resultados.html'

    def get(self, request, *args, **kwargs):
        clase_virtual = models.ClaseVirtual.objects.filter(pk=self.kwargs['pk']).first()
        alumno = self.request.user.alumno
        respuestas = models.RespuestaEjercicioVirtual.objects.filter(clase_virtual=clase_virtual)\
            .filter(alumno=alumno)
        return render(request, self.template_name, {
                            'clase_virtual':clase_virtual,
                            'respuestas': respuestas
                            })


class ClaseVirtualCorreccionListView(View):
    template_name = 'clase_virtual/clase_virtual_resultados_list.html'
    def get(self, request, *args, **kwargs):
        clase_virtual = models.ClaseVirtual.objects.filter(pk=self.kwargs['pk']).first()
        alumnos = models.Alumno.objects.filter(inscripciones__instancia_cursado__materia = clase_virtual.materia)
        respuestas_realizadas = models.RespuestaEjercicioVirtual.objects.filter(clase_virtual=clase_virtual)\
            .filter(alumno__in=alumnos).values('alumno').annotate(num_respuestas=Count("alumno")).distinct()
        respuestas_correctas = models.RespuestaEjercicioVirtual.objects.filter(clase_virtual=clase_virtual)\
            .filter(es_correcta=True)\
            .filter(alumno__in=alumnos).values('alumno').annotate(num_correctas=Count("alumno")).distinct()
        return render(request, self.template_name, {
                            'clase_virtual':clase_virtual,
                            'alumnos': alumnos,
                            'respuestas_realizadas': respuestas_realizadas,
                            'respuestas_correctas': respuestas_correctas
                        })


class ClaseVirtualCorreccionResultadosView(View):
    template_name = 'clase_virtual/clase_virtual_corregir_resultados.html'

    def get(self, request, *args, **kwargs):
        clase_virtual = models.ClaseVirtual.objects.filter(pk=self.kwargs['pk']).first()
        alumno = models.Alumno.objects.filter(pk=self.kwargs['alumno_pk']).first()
        respuestas = models.RespuestaEjercicioVirtual.objects.filter(clase_virtual=clase_virtual)\
            .filter(alumno=alumno)
        formset = CorregirRespuestaEjercicioVirtualFormSet(queryset=respuestas)

        return render(request, self.template_name, {
                                'clase_virtual':clase_virtual,
                                'respuestas': respuestas,
                                'formset': formset
                            })

    def post(self, request, *args, **kwargs):
        clase_virtual = models.ClaseVirtual.objects.filter(pk=self.kwargs['pk']).first()
        alumno = models.Alumno.objects.filter(pk=self.kwargs['alumno_pk']).first()
        respuestas = models.RespuestaEjercicioVirtual.objects.filter(clase_virtual=clase_virtual)\
            .filter(alumno=alumno)
        formset = CorregirRespuestaEjercicioVirtualFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return render(request, self.template_name, {
                        'clase_virtual':clase_virtual,
                        'respuestas': respuestas,
                        'formset': formset
                    })
        else:
            return render(request, self.template_name, {
                    'clase_virtual':clase_virtual,
                    'respuestas': respuestas,
                    'formset': formset
                })
        return;


class ClaseVirtualResolverEjercicioView(View):
     def post(self, request, *args, **kwargs):
        clase_virtual = models.ClaseVirtual.objects.filter(pk=self.kwargs['pk'])
        ejercicio_a_resolver = None
        form_to_render = None
        template_to_render = None
        ejercicio_to_render = None
        tipoPreguntaToRender = None
        es_correcta = None
        if('ejercicioId' in request.POST and 'tipoPregunta' in request.POST):
            form = None
            ejercicio_resuelto = None
            if(request.POST['tipoPregunta'] == 'texto'):
                form = RespuestaEjercicioVirtualTextoForm(request.POST, request.FILES)
                ejercicio_resuelto = models.EjercicioVirtualTexto.objects.filter(id=request.POST['ejercicioId'])
                template_to_render = 'ejercicio_virtual/texto/resolver_ejercicio_virtual_form.html'
                tipoPreguntaToRender = 'texto'
                es_correcta = None
            elif(request.POST['tipoPregunta'] == 'multiple_choice'):
                template_to_render = 'ejercicio_virtual/multiple_choice/resolver_ejercicio_virtual_form.html'
                tipoPreguntaToRender = 'multiple_choice'
                form = RespuestaEjercicioVirtualMultipleChoiceForm(request.POST, request.FILES)
                ejercicio_resuelto = models.EjercicioVirtualMultipleChoice.objects.filter(id=request.POST['ejercicioId'])
                es_correcta = form.instance.opcion_seleccionada.opcion_correcta
            if form.is_valid():
                form.instance.alumno = self.request.user.alumno
                form.instance.ejercicio = ejercicio_resuelto.first()
                form.instance.clase_virtual = clase_virtual.first()
                form.instance.es_correcta = es_correcta
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
                                            })
        else:
            ejercicio_a_resolver = clase_virtual.first().ejercicios.first()
        if(ejercicio_a_resolver == None):
            return redirect('aula_virtual:resultados_clase_virtual', pk=clase_virtual.first().id)
        elif(ejercicio_a_resolver.is_ejercicio_virtual_multiple_choice()):
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

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ClaseVirtualUpdateView, self).get_form_kwargs(**kwargs)
        kwargs['profesor'] = self.request.user.profesor
        return kwargs


class ClaseVirtualDeleteView(ProtectedDeleteView):
    model = models.ClaseVirtual
    success_url = reverse_lazy('aula_virtual:clases_virtuales')
    template_name = 'clase_virtual/clase_virtual_confirm_delete.html'


class EjercicioVirtualCreateView(CreateView):
    model = models.EjercicioVirtual
    form_class = forms.EjercicioVirtualForm
    template_name = 'ejercicio_virtual/ejercicio_virtual_form.html'

    def form_valid(self, form):
        clase_virtual = models.ClaseVirtual.objects.get(pk=self.kwargs['clase_id'])
        form.instance.clase_virtual = clase_virtual
        return super(EjercicioVirtualCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('aula_virtual:ver_clase_virtual', kwargs={'pk': self.object.clase_virtual.id})


class EjercicioVirtualTextoCreateView(CreateView):
    model = models.EjercicioVirtualTexto
    form_class = forms.EjercicioVirtualTextoForm
    template_name = 'ejercicio_virtual/texto/ejercicio_virtual_form.html'

    def form_valid(self, form):
        clase_virtual = models.ClaseVirtual.objects.get(pk=self.kwargs['clase_id'])
        form.instance.clase_virtual = clase_virtual
        return super(EjercicioVirtualTextoCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('aula_virtual:ver_clase_virtual', kwargs={'pk': self.object.clase_virtual.id})


class EjercicioVirtualTextoUpdateView(UpdateView):
    model = models.EjercicioVirtualTexto
    form_class=forms.EjercicioVirtualTextoForm
    template_name = 'ejercicio_virtual/texto/ejercicio_virtual_form.html'

    def get_success_url(self):
        return reverse_lazy('aula_virtual:ver_clase_virtual', kwargs={'pk': self.object.clase_virtual.id})


class EjercicioVirtualMultipleChoiceCreateView(CreateView):
    model = models.EjercicioVirtualMultipleChoice
    form_class = forms.EjercicioVirtualMultipleChoiceForm
    template_name = 'ejercicio_virtual/multiple_choice/ejercicio_virtual_form.html'

    def get_success_url(self):
        return reverse_lazy('aula_virtual:ver_clase_virtual', kwargs={'pk': self.object.clase_virtual.id})

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        opcion_formset = OpcionEjercicioVirtualFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  opcion_formset=opcion_formset))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        opcion_formset = OpcionEjercicioVirtualFormSet(self.request.POST)
        if (form.is_valid() and opcion_formset.is_valid()):
            return self.form_valid(form, opcion_formset)
        else:
            return self.form_invalid(form, opcion_formset)

    def form_valid(self, form, opcion_formset):
        clase_virtual = models.ClaseVirtual.objects.get(pk=self.kwargs['clase_id'])
        form.instance.clase_virtual = clase_virtual
        self.object = form.save()
        opcion_formset.instance = self.object
        opcion_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, opcion_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  opcion_formset=opcion_formset))


class EjercicioVirtualMultipleChoiceUpdateView(UpdateView):
    model = models.EjercicioVirtualMultipleChoice
    form_class = forms.EjercicioVirtualMultipleChoiceForm
    template_name = 'ejercicio_virtual/multiple_choice/ejercicio_virtual_form.html'

    def get_success_url(self):
        return reverse_lazy('aula_virtual:ver_clase_virtual', kwargs={'pk': self.object.clase_virtual.id})

    def get(self, request, *args, **kwargs):
        self.object = self.model.objects.filter(pk= self.kwargs['pk']).first()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        opcion_formset = OpcionEjercicioVirtualUpdateFormSet(instance=self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  opcion_formset=opcion_formset))

    def post(self, request, *args, **kwargs):
        self.object = self.model.objects.filter(pk= self.kwargs['pk']).first()
        clase_virtual = models.ClaseVirtual.objects.get(pk= self.object.clase_virtual.id)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.instance.clase_virtual = clase_virtual
        opcion_formset = OpcionEjercicioVirtualFormSet(self.request.POST, instance = self.object)
        if (form.is_valid() and opcion_formset.is_valid()):
            return self.form_valid(form, opcion_formset)
        else:
            return self.form_invalid(form, opcion_formset)

    def form_valid(self, form, opcion_formset):
        self.object = form.save()
        opcion_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, opcion_formset):
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
