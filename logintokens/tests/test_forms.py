"""logintokens app unittests for forms

"""
import re

from django.test import TestCase, RequestFactory
from django.core import mail
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from logintokens.forms import TokenLoginForm


USER = get_user_model()


class LoginFormTest(TestCase):
    """Tests the form which validates the email used for login.

    """
    def setUp(self):
        self.existing_user = USER._default_manager.create_user(
            'loginformtest-existinguser',
            'loginformtest-existinguser@example.com')
        self.test_email = 'newvisitor@example.com'
        self.request = RequestFactory().get('/')

    def test_valid_email_accepted(self):
        form = TokenLoginForm({'email': self.test_email})
        self.assertTrue(form.is_valid())

    def test_can_send_email(self):
        form = TokenLoginForm({'email': self.test_email})
        if form.is_valid():
            form.save(self.request)
        self.assertEqual(len(mail.outbox), 1)

    def test_email_contains_link(self):
        form = TokenLoginForm({'email': self.test_email})
        if form.is_valid():
            form.save(self.request)
        email = mail.outbox[0]
        url_search = re.search(r'https?://.+/.+$', email.body)
        self.assertIsNotNone(url_search)
        url = url_search.group(0)
        self.assertIn(reverse('token_login'), url)

    def test_normal_user(self):
        """The link is sent to the user's email not to their username.

        """
        form = TokenLoginForm({'email': self.existing_user.get_username()})
        if form.is_valid():
            form.save(self.request)
        email = mail.outbox[0]
        self.assertEqual(
            email.to,
            [getattr(self.existing_user, USER.EMAIL_FIELD)])
