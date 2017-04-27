"""views for accounts app

"""
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.edit import FormView

from logintokens.forms import TokenLoginForm


class TokenLoginView(RedirectView):
    pattern_name = 'home'

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        if token:
            user = authenticate(token=token)
            if user:
                login(request, user)
        return super(TokenLoginView, self).get(request, *args, **kwargs)


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


class SendTokenDoneView(TemplateView):
    template_name = 'logintokens/send_token_done.html'
    title = 'Login token sent'
