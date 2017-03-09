"""accounts app unittests

"""
from django.test import TestCase


class WelcomePageTest(TestCase):
    def test_uses_welcome_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'accounts/welcome.html')
