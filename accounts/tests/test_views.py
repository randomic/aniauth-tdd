"""accounts app unittests for views

"""
from django.test import TestCase
from django.core import mail
from django.shortcuts import reverse


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

    def test_redirects_to_emailsent(self):
        """The send_login_email url redirects to login_email_sent.

        """
        response = self.client.post(self.url, data={'email': self.test_email})
        self.assertRedirects(response, reverse('login_email_sent'))

    def test_invalid_email_redirect(self):
        """Invalid email is posted the view should redirect welcome view.

        """
        response = self.client.post(self.url, data={'email': 'invalidemail'})
        self.assertRedirects(response, reverse('welcome'))

    def test_get_request_yields_405(self):
        """Accessing the view via get request is not allowed.

        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_view_sends_token_email(self):
        """The view should send an email to the email address from post.

        """
        self.client.post(self.url, data={'email': self.test_email})
        self.assertEqual(mail.outbox[0].to, [self.test_email])


class LoginEmailSentTest(TestCase):
    """Tests for the view which displays success message.

    """
    def test_uses_correct_template(self):
        """The view should use the template which contains a success message.

        """
        response = self.client.get(reverse('login_email_sent'))
        self.assertTemplateUsed(response, 'accounts/login_email_sent.html')
        self.assertContains(response, 'Check your email')


class LoginViewTest(TestCase):
    """Tests for the view which verifies tokens and allows users to login.

    """
    def test_uses_correct_template(self):
        """The view should use the template which contains a login button.

        """
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'accounts/login.html')
