from gutils.django.views.generic import FilterMixin

__author__ = 'rmotteta'

from gutils.django.views import ProtectedDeleteView

from django.views.generic import ListView, CreateView, UpdateView, \
    TemplateView,DetailView,View

class CreateView(CreateView):

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['kwargs'] = self.kwargs
        return context


class UpdateView(UpdateView):

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ProtectedDeleteView(ProtectedDeleteView):

    def get_context_data(self, **kwargs):
        context = super(ProtectedDeleteView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class TemplateView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class DetailView(DetailView):

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ListView(ListView):

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class FilteredListView(ListView, FilterMixin):
    """
    This class is used to extend listviews adding a filter_form to the template
    Needed attributes:
    - form_class: the form defined to filter the view
    - model: the model that is displayed

    Note:
    In the Meta class of the form, a dict called filters can be defined to specify the behavior.
    The key is the name of the field, while the value is the kwarg used in the queryset.
    If the field is not present in this dictionary, the lookup defaults to 'form_field_name=value'
    Example:

    class FilterForm(forms.BaseForm):
        date_from = forms.DateField()
        date_to = forms.DateField()
        value = forms.FloatField()
        price = forms.FloatField()

        class Meta:
            filters = {
                'date_from': 'date__gte',
                'date_to': 'date__lte',
                'value': 'model_value',
            }

    This generates the queryset: model.objects.filter(date__gte=date_from).filter(dete__lte=date_to).
                                      filter(model_value=value).filter(price=price)
    """
    def get_context_data(self, **kwargs):
        context = super(FilteredListView, self).get_context_data(**kwargs)
        context['filter_form'] = self._filtro_form
        return context

    def get_queryset(self):
        return self._filter_queryset(self.request)