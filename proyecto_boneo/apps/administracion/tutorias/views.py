from . import forms, models

# Create your views here.
import datetime
from django.core.urlresolvers import reverse_lazy
from django.forms import formset_factory, model_to_dict
from django.shortcuts import render, redirect
from gutils.django.views import View
from proyecto_boneo.apps.administracion.alumnos.models import Alumno
from proyecto_boneo.apps.administracion.personal.models import Profesor
from proyecto_boneo.apps.administracion.tutorias.forms import TutoriaForm, EncuentroTutoriaForm, \
    EncuentroTutoriaForTutoriaForm
from proyecto_boneo.apps.administracion.usuarios.customViews.views import ListView, CreateView, DetailView, UpdateView, \
    ProtectedDeleteView


class TutoriasListView(ListView):
    model = models.Tutoria
    template_name = 'tutorias/tutorias_list.html'

class TutoriasAlumnoListView(ListView):
    model = models.Tutoria
    template_name = 'tutorias/tutorias_list.html'

    def get_queryset(self):
        self.alumno = Alumno.objects.get(usuario_id=self.request.user.id)
        return models.Tutoria.objects.filter(alumno=self.alumno)


class TutoriasProfesorListView(ListView):
    model = models.Tutoria
    template_name = 'tutorias/tutorias_list.html'

    def get_queryset(self):
        self.profesor = Profesor.objects.get(usuario_id=self.request.user.id)
        return models.Tutoria.objects.filter(profesor=self.profesor)


class TutoriaCreateView(CreateView):
    model = models.Tutoria
    success_url = reverse_lazy('administracion:tutorias')
    form_class = forms.TutoriaForm
    template_name = 'tutorias/tutorias_form.html'


class TutoriaDetailView(View):
    # model = models.Tutoria
    # # success_url = reverse_lazy('administracion:tutorias')
    # form_class = forms.TutoriaForm
    template_name = 'tutorias/tutorias_view.html'

    def get(self, request, *args, **kwargs):
        tutoria = models.Tutoria.objects.get(pk=self.kwargs['pk'])
        EncuentroTutoriaFormSet = formset_factory(EncuentroTutoriaForTutoriaForm)
        formset = EncuentroTutoriaFormSet()
        return render(request, self.template_name, {'object': tutoria,
                                                    'formset':formset,
                                                    'user': self.request.user
                                                    } )

    def post(self, request, *args, **kwargs):
        EncuentroTutoriaFormSet = formset_factory(EncuentroTutoriaForTutoriaForm)
        formset = EncuentroTutoriaFormSet(request.POST, request.FILES)
        tutoria = models.Tutoria.objects.get(pk=self.kwargs['pk'])
        # check whether it's valid:
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    # if form.cleaned_data.get('DELETE') and form.instance.pk:
                    #     form.instance.delete()
                    # else:
                    instance = form.save(commit=False)
                    instance.tutoria = tutoria
                    instance.save()
            formset = EncuentroTutoriaFormSet()
            return render(request, self.template_name, {
                            'object': tutoria,
                            'formset':formset,
                            'user': self.request.user
                })

        # if formset.is_valid():
        #     nueva_tutoria = formset.save()

        # else:
        #     rechazo_solicitud_form = SolicitudMaterialRechazoForm(instance = solicitud_material)
        #     return render(request, self.template_name, {'solicitud_material': solicitud_material,
        #                 'form':form,
        #                 'rechazo_solicitud_form': rechazo_solicitud_form,
        #                 'user': self.request.user
        #                 } )


class TutoriaUpdateView(UpdateView):
    model = models.Tutoria
    success_url = reverse_lazy('administracion:tutorias')
    form_class = forms.TutoriaForm
    template_name = 'tutorias/tutorias_form.html'


class TutoriaDeleteView(ProtectedDeleteView):
    model = models.Tutoria
    success_url = reverse_lazy('administracion:tutorias')
    template_name = 'tutorias/tutorias_confirm_delete.html'


class EncuentroTutoriasListView(ListView):
    model = models.EncuentroTutoria
    template_name = 'encuentrotutorias/encuentrotutorias_list.html'


class EncuentroTutoriaCreateView(CreateView):
    model = models.EncuentroTutoria
    success_url = reverse_lazy('administracion:encuentrotutorias')
    form_class = forms.EncuentroTutoriaForm
    template_name = 'encuentrotutorias/encuentrotutorias_form.html'


class EncuentroTutoriaDetailView(DetailView):
    model = models.EncuentroTutoria
    # success_url = reverse_lazy('administracion:encuentrotutorias')
    form_class = forms.EncuentroTutoriaForm
    template_name = 'encuentrotutorias/encuentrotutorias_view.html'


class EncuentroTutoriaUpdateView(UpdateView):
    model = models.EncuentroTutoria
    success_url = reverse_lazy('administracion:encuentrotutorias')
    form_class = forms.EncuentroTutoriaForm
    template_name = 'encuentrotutorias/encuentrotutorias_form.html'


class EncuentroTutoriaDeleteView(ProtectedDeleteView):
    model = models.EncuentroTutoria
    success_url = reverse_lazy('administracion:encuentrotutorias')
    template_name = 'encuentrotutorias/encuentrotutorias_confirm_delete.html'