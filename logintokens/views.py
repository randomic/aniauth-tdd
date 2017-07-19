"""views for accounts app

"""
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.edit import FormView

from logintokens.forms import TokenLoginForm
from logintokens.tokens import default_token_generator


class TokenLoginView(RedirectView):
    """Handles the token-based login process.

    """
    pattern_name = 'home'

    def get(self, request, *args, **kwargs):
        """Attempt to log the token's user in.

        """
        token = request.GET.get('token')
        if token:
            user = authenticate(request, token=token)
            if user:
                login(request, user)
        return super(TokenLoginView, self).get(request, *args, **kwargs)


class SendTokenView(FormView):
    """Display and process the login token form.

    """
    email_template_content = 'logintokens/login_token_email_content.txt'
    email_template_subject = 'logintokens/login_token_email_subject.txt'
    form_class = TokenLoginForm
    from_email = None
    success_url = reverse_lazy('send_token_done')
    template_name = 'logintokens/send_token_form.html'
    title = 'Send login token'
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(SendTokenView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'email_templates': {
                'subject': self.email_template_subject,
                'content': self.email_template_content,
            },
            'from_email': self.from_email,
            'request': self.request,
            'token_generator': self.token_generator,

        }
        form.save(**opts)
        return super(SendTokenView, self).form_valid(form)


class SendTokenDoneView(TemplateView):
    """Displays a success message indicating a login token has been sent.

    """
    template_name = 'logintokens/send_token_done.html'
    title = 'Login token sent'
