"""forms for accounts app

"""
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy

from logintokens.tokens import default_token_generator


USER = get_user_model()


class TokenLoginForm(forms.Form):
    email = UsernameField(  # For the majority of users it will be an email.
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True}),
    )

    def clean(self):
        # Some users will have a username different from their email.
        email = self.cleaned_data['email']
        try:
            user = USER._default_manager.get_by_natural_key(email)
            clean_email = getattr(user, USER.EMAIL_FIELD)
        except USER.DoesNotExist:
            clean_email = email
        validate_email(clean_email)
        self.cleaned_data['clean_email'] = clean_email
        return self.cleaned_data

    def generate_login_link(self, username, request):
        protocol = 'https' if request.is_secure() else 'http'
        domain = get_current_site(request).domain
        url = reverse_lazy('token_login')
        token = default_token_generator.make_token(username)
        return '{}://{}{}?token={}'.format(protocol, domain, url, token)

    def save(self, request):
        """Generate a login token and send it to the email from the form.

        """
        email = self.cleaned_data['email']
        clean_email = self.cleaned_data['clean_email']

        body = 'To complete the login process, simply click on this link: {}'
        login_link = self.generate_login_link(email, request)

        email_message = EmailMultiAlternatives(
            'Your login link for ANIAuth',
            body.format(login_link),
            to=[clean_email]
        )
        email_message.send()
