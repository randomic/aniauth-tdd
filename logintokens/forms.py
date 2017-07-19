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


class EmailOrUsernameField(UsernameField):

    def clean(self, value):
        value = super(EmailOrUsernameField, self).clean(value)
        try:
            # pylint: disable=protected-access
            user = USER._default_manager.get_by_natural_key(value)
            email = getattr(user, USER.EMAIL_FIELD)
        except USER.DoesNotExist:
            email = value
        validate_email(email)
        return (value, email)


class TokenLoginForm(forms.Form):
    email = EmailOrUsernameField(  # For the majority of users it will be an email.
        max_length=254
    )

    def generate_login_link(self, username, request):
        protocol = 'https' if request.is_secure() else 'http'
        domain = get_current_site(request).domain
        url = reverse_lazy('token_login')
        token = default_token_generator.make_token(username)
        return '{}://{}{}?token={}'.format(protocol, domain, url, token)

    def save(self, request):
        """Generate a login token and send it to the email from the form.

        """
        value, email = self.cleaned_data['email']

        body = 'To complete the login process, simply click on this link: {}'
        login_link = self.generate_login_link(value, request)

        email_message = EmailMultiAlternatives(
            'Your login link for ANIAuth',
            body.format(login_link),
            to=[email]
        )
        email_message.send()
