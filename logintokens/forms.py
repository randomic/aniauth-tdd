"""forms for accounts app

"""
from django import forms
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import FormActions

from logintokens.tokens import default_token_generator


USER = get_user_model()


class EmailOrUsernameField(UsernameField):
    """Specialised field which fetches the user's email address when cleaned.

    """
    def clean(self, value):
        """If user exists fetch their email.

        If the value is the username of an existing user, return a tuple
        containing the username and the user's email address.

        If the value is not the username of an existing user, check that it is
        and email address and return a tuple containing two copies of it. This
        is so that a new user can be created.

        """
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
    """Sends a login link to the user specified in the only field.

    """
    email = EmailOrUsernameField(  # For majority of users it will be an email.
        max_length=254
    )

    @property
    def helper(self):
        """Helper for rendering crispy form.

        """
        helper = FormHelper()
        helper.form_show_labels = False
        helper.layout = Layout(
            Field('email', placeholder='Email'),
            FormActions(
                Submit('submit', 'Login', css_class='btn btn-outline-success')
            ))
        return helper

    @staticmethod
    def send_mail(email_template_subject, email_template_content,
                  context, from_email, to_email):
        """Sends a django.core.mail.EmailMultiAlternatives to `to_email`.

        """
        subject = loader.render_to_string(email_template_subject, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_content, context)

        email_message = EmailMultiAlternatives(
            subject, body, from_email, [to_email])
        email_message.send()

    def save(
            self, email_templates=None, from_email=None,
            token_generator=default_token_generator, request=None):
        """Generate a login token and send it to the email from the form.

        """
        email_templates = email_templates or {
            'subject': 'logintokens/login_token_email_subject.txt',
            'content': 'logintokens/login_token_email_content.txt',
        }
        username, email = self.cleaned_data["email"]

        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain

        context = {
            'site_name': site_name,
            'protocol': 'https' if request.is_secure() else 'http',
            'domain': domain,
            'token': token_generator.make_token(username),
        }
        self.send_mail(email_templates['subject'],
                       email_templates['content'],
                       context, from_email, email)
