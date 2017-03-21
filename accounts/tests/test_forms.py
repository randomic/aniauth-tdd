"""accounts app unittests for forms

"""
from django.test import TestCase

from accounts.forms import LoginForm


class LoginFormTest(TestCase):
    """Tests the form which validates the email used for login.

    """
    def test_valid_email_accepted(self):
        form = LoginForm({'email': 'newvisitor@example.com'})
        self.assertTrue(form.is_valid())

    def test_invalid_email_declined(self):
        form = LoginForm({'email': 'invalidemail'})
        self.assertFalse(form.is_valid())
