from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy

from evexml.forms import AddAPIForm


class AddAPIView(FormView):
    template_name = 'evexml/eveapi_add_form.html'
    form_class = AddAPIForm
    success_url = reverse_lazy('eveapi_added')

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(AddAPIView, self).dispatch(*args, **kwargs)


class AddedAPIView(TemplateView):
    template_name = 'evexml/eveapi_added.html'
