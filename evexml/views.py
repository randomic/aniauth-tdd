from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy

from evexml.forms import AddAPIForm


class AddAPIView(FormView):
    template_name = 'evexml/eveapi_add_form.html'
    form_class = AddAPIForm
    success_url = reverse_lazy('eveapi_added')


class AddedAPIView(TemplateView):
    template_name = 'evexml/eveapi_added.html'
