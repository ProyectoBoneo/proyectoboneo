from datetime import datetime
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from proyecto_boneo.apps.administracion.usuarios.customViews.views import CreateView, UpdateView, ProtectedDeleteView, FilteredListView, ListView, DetailView, \
    TemplateView
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

    def get_queryset(self):
        if(self.request.user.is_staff):
            return models.ClaseVirtual.objects.all()
        if(self.request.user.is_alumno):
            return models.ClaseVirtual.objects.filter(materia__instancias_cursado__inscripciones__alumno=self.request.user.alumno).distinct()
        if(self.request.user.is_profesor):
            return models.ClaseVirtual.objects.filter(materia__instancias_cursado__profesor_titular=self.request.user.profesor).distinct()


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
        alumnos = models.Alumno.objects.filter(inscripciones__instancia_cursado__materia=clase_virtual.materia)\
            .filter(inscripciones__instancia_cursado__anio_cursado=datetime.today().year).distinct()

        for alumno in alumnos:
            try:
                alumno.nota_actual = models.ResultadoEvaluacion.objects.get(alumno=alumno,
                                                                            clase_virtual=clase_virtual).nota
            except models.ResultadoEvaluacion.DoesNotExist:
                alumno.nota_actual = None

        return render(request, self.template_name, {
                            'clase_virtual': clase_virtual,
                            'alumnos': alumnos,
                        })


class ClaseVirtualCorreccionResultadosView(View):
    template_name = 'clase_virtual/clase_virtual_corregir_resultados.html'
    template_name_evaluacion = 'clase_virtual/clase_virtual_corregir_evaluacion_escrita.html'

    def get(self, request, *args, **kwargs):
        clase_virtual = models.ClaseVirtual.objects.filter(pk=self.kwargs['pk']).first()
        alumno = models.Alumno.objects.filter(pk=self.kwargs['alumno_pk']).first()

        if clase_virtual.tipo == models.ClaseVirtual.EVALUACION_ESCRITA:
            try:
                resultado = models.ResultadoEvaluacion.objects.get(alumno=alumno, clase_virtual=clase_virtual)
            except models.ResultadoEvaluacion.DoesNotExist:
                resultado = None
            form = forms.CorregirEvaluacionEscritaForm(initial={'nota': resultado.nota if resultado else None})
            return render(request, self.template_name_evaluacion, {'clase_virtual': clase_virtual, 'form': form})
        else:
            respuestas = models.RespuestaEjercicioVirtual.objects.filter(clase_virtual=clase_virtual)\
                .filter(alumno=alumno)
            formset = CorregirRespuestaEjercicioVirtualFormSet(queryset=respuestas)
            return render(request, self.template_name, {
                                    'clase_virtual': clase_virtual,
                                    'respuestas': respuestas,
                                    'formset': formset
                                })

    def update_resultado_evaluacion(self, clase_virtual, alumno, nota):
        models.ResultadoEvaluacion.objects.update_or_create(clase_virtual=clase_virtual, alumno=alumno,
                                                            defaults={'nota': nota})

    def update_resultados(self, clase_virtual, alumno, respuestas):
        if clase_virtual.tipo == models.ClaseVirtual.EVALUACION:
            total = len(respuestas)
            correctas = len(respuestas.filter(es_correcta=True))
            self.update_resultado_evaluacion(clase_virtual, alumno, round((correctas/total)*10, 2))

    def post(self, request, *args, **kwargs):
        clase_virtual = models.ClaseVirtual.objects.filter(pk=self.kwargs['pk']).first()
        alumno = models.Alumno.objects.filter(pk=self.kwargs['alumno_pk']).first()

        if clase_virtual.tipo == models.ClaseVirtual.EVALUACION_ESCRITA:
            form = forms.CorregirEvaluacionEscritaForm(request.POST)
            if form.is_valid():
                self.update_resultado_evaluacion(clase_virtual, alumno, form.cleaned_data['nota'])
                return redirect(reverse_lazy('aula_virtual:corregir_resultados_clase_virtual',
                                             kwargs={'pk': clase_virtual.id}))
            else:
                return render(request, self.template_name_evaluacion, {'clase_virtual': clase_virtual, 'form': form})
        else:
            respuestas = models.RespuestaEjercicioVirtual.objects.filter(clase_virtual=clase_virtual, alumno=alumno)
            formset = CorregirRespuestaEjercicioVirtualFormSet(request.POST)
            if formset.is_valid():
                formset.save()
                self.update_resultados(clase_virtual, alumno, respuestas)
                return redirect(reverse_lazy('aula_virtual:corregir_resultados_clase_virtual',
                                             kwargs={'pk': clase_virtual.id}))
            else:
                return render(request, self.template_name, {
                        'clase_virtual': clase_virtual,
                        'respuestas': respuestas,
                        'formset': formset
                    })


def obtener_siguiente_ejercicio_a_resolver(clase_virtual):
    ejercicios = clase_virtual.ejercicios.all()
    for ejercicio in ejercicios:
        if not ejercicio.ejercicio_instance().respuestas.all().exists():
            return ejercicio
    return None


class ClaseVirtualResolverEjercicioView(View):
     def post(self, request, *args, **kwargs):
        clase_virtual = models.ClaseVirtual.objects.filter(pk=self.kwargs['pk']).first()
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
                ejercicio_resuelto = models.EjercicioVirtualTexto.objects.filter(id=request.POST['ejercicioId']).first()
                template_to_render = 'ejercicio_virtual/texto/resolver_ejercicio_virtual_form.html'
                tipoPreguntaToRender = 'texto'
                es_correcta = None
            elif(request.POST['tipoPregunta'] == 'multiple_choice'):
                template_to_render = 'ejercicio_virtual/multiple_choice/resolver_ejercicio_virtual_form.html'
                tipoPreguntaToRender = 'multiple_choice'
                form = RespuestaEjercicioVirtualMultipleChoiceForm(request.POST, request.FILES)
                ejercicio_resuelto = models.EjercicioVirtualMultipleChoice.objects.filter(id=request.POST['ejercicioId']).first()
                es_correcta = form.instance.opcion_seleccionada.opcion_correcta
            if form.is_valid():
                form.instance.alumno = self.request.user.alumno
                form.instance.ejercicio = ejercicio_resuelto
                form.instance.clase_virtual = clase_virtual
                form.instance.es_correcta = es_correcta
                nueva_respuesta = form.save()
                obtener_siguiente_ejercicio_a_resolver(clase_virtual)
                ejercicio_a_resolver = obtener_siguiente_ejercicio_a_resolver(clase_virtual)
            else:
                return render(request, template_to_render, {
                                            'form':form_to_render,
                                            'ejercicio': ejercicio_resuelto,
                                            'tipoPregunta': tipoPreguntaToRender,
                                            'user': self.request.user
                                            })
        else:
            ejercicio_a_resolver = obtener_siguiente_ejercicio_a_resolver(clase_virtual)
        if(ejercicio_a_resolver == None):
            return redirect('aula_virtual:resultados_clase_virtual', pk=clase_virtual.id)
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


class ClaseVirtualAyudaTemplateView(TemplateView):
    template_name = 'clase_virtual/clase_virtual_ayuda_list.html'

class ClaseVirtualAyudaVerTemplateView(TemplateView):
    template_name = 'clase_virtual/clase_virtual_ayuda_ver.html'

class ClaseVirtualAyudaNuevoTemplateView(TemplateView):
    template_name = 'clase_virtual/clase_virtual_ayuda_nuevo.html'

class ClaseVirtualAyudaEditarTemplateView(TemplateView):
    template_name = 'clase_virtual/clase_virtual_ayuda_editar.html'

class ClaseVirtualAyudaEliminarTemplateView(TemplateView):
    template_name = 'clase_virtual/clase_virtual_ayuda_eliminar.html'