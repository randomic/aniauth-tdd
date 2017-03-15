"""accounts app unittests for views

"""
from django.test import TestCase


class WelcomePageTest(TestCase):
    """Tests relating to the welcome_page view.

    """
    def test_uses_welcome_template(self):
        """The root url should response with the welcome page template.

        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'accounts/welcome.html')
