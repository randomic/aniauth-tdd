"""views for accounts app

"""
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.edit import BaseFormView
from django.http import HttpResponseRedirect
from django.contrib import messages

from logintokens.forms import TokenLoginForm


class TokenLoginView(RedirectView):
    pattern_name = 'home'

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        if token:
            user = authenticate(request, token=token)
            if user:
                login(request, user)
        return super(TokenLoginView, self).get(request, *args, **kwargs)


class SendTokenView(BaseFormView):
    form_class = TokenLoginForm
    success_url = reverse_lazy('home')
    title = 'Send login token'

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save(self.request)
        messages.success(self.request, 'Check your email! A link has been sent to you, click on this link to complete the login process.')
        return super(SendTokenView, self).form_valid(form)

    def form_invalid(self, form):
        """If the form is valid, redirect to the supplied URL with errors.

        """
        for dummy_field, error in form.errors.items():
            messages.warning(self.request, error.as_text())
        return HttpResponseRedirect(self.get_success_url())


class SendTokenDoneView(TemplateView):
    template_name = 'logintokens/send_token_done.html'
    title = 'Login token sent'
