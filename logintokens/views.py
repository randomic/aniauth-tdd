"""views for accounts app

"""
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView

from logintokens.forms import TokenLoginForm


class SendTokenView(FormView):
    form_class = TokenLoginForm
    success_url = reverse_lazy('send_token_done')
    template_name = 'logintokens/send_token_form.html'
    title = 'Send login token'

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save(self.request)
        return super(SendTokenView, self).form_valid(form)


def login_email_sent(request):
    return render(request, 'accounts/login_email_sent.html')


def login(request):
    return render(request, 'accounts/login.html')
