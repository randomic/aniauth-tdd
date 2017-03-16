"""accounts app unittests for views

"""
from django.test import TestCase
from django.urls import reverse


class WelcomePageTest(TestCase):
    """Tests relating to the welcome_page view.

    """
    def test_uses_welcome_template(self):
        """The root url should respond with the welcome page template.

        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'accounts/welcome.html')


class SendLoginEmailTest(TestCase):
    """Tests for the view which sends the login email.

    """
    def setUp(self):
        self.url = reverse('send_login_email')
        self.test_email = 'newvisitor@example.com'

    def test_uses_emailsent_template(self):
        """The send_login_email url responds with login_email_sent template.

        """
        response = self.client.post(self.url, data={'email': self.test_email})
        self.assertTemplateUsed(response, 'accounts/login_email_sent.html')

    def test_get_request_yields_405(self):
        """Accessing the view via get request is not allowed.

        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

