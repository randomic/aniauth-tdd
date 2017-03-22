"""forms for accounts app

"""
from django import forms
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy

from accounts.tokens import LoginTokenGenerator


USER = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)

    def generate_login_link(self, email, request):
        protocol = 'http'
        domain = get_current_site(request).domain
        url = reverse_lazy('login')
        token = LoginTokenGenerator().make_token(email)
        return '{}://{}{}?token={}'.format(protocol, domain, url, token)

    def save(self, request):
        """Generate a login token and send it to the email from the form.

        """
        email = self.cleaned_data['email']
        body = 'To complete the login process, simply click on this link: {}'
        login_link = self.generate_login_link(email, request)

        email_message = EmailMultiAlternatives(
            'Your login link for ANIAuth',
            body.format(login_link),
            to=[email]
        )
        email_message.send()
