"""logintokens app unittests for views

"""
from django.test import TestCase
from django.core import mail
from django.shortcuts import reverse


class TokenLoginViewTest(TestCase):
    """Tests for the view which verifies tokens and allows users to login.

    """
    def test_redirects_to_home(self):
        """The view should eventually redirect to the homepage.

        """
        response = self.client.get(reverse('token_login'))
        self.assertRedirects(response, reverse('home'))


class SendTokenViewTest(TestCase):
    """Tests for the view which sends the login email.

    """
    def setUp(self):
        self.url = reverse('send_token')
        self.test_email = 'newvisitor@example.com'

    def test_redirects_send_token_done(self):
        """The send_login_email url redirects to success page.

        """
        response = self.client.post(self.url, data={'email': self.test_email})
        self.assertRedirects(response, reverse('send_token_done'))

    def test_view_sends_token_email(self):
        """The view should send an email to the email address from post.

        """
        self.client.post(self.url, data={'email': self.test_email})
        self.assertEqual(mail.outbox[0].to, [self.test_email])


class SendTokenDoneViewTest(TestCase):
    """Tests for the view which displays success message.

    """
    def test_uses_correct_template(self):
        """The view should use the template which contains a success message.

        """
        response = self.client.get(reverse('send_token_done'))
        self.assertTemplateUsed(response, 'logintokens/send_token_done.html')
        self.assertContains(response, 'Check your email')
