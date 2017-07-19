"""logintokens app unittests for views

"""
from django.test import TestCase
from django.contrib.auth import get_user_model, get_user
from django.core import mail
from django.shortcuts import reverse

from logintokens.tokens import default_token_generator


USER = get_user_model()


class TokenLoginViewTest(TestCase):
    """Tests for the view which verifies tokens and allows users to login.

    """
    def setUp(self):
        # pylint: disable=protected-access
        self.url = reverse('token_login')
        self.generator = default_token_generator
        self.new_username = 'tokenloginviewtest-newvisitor'
        self.existing_user = USER._default_manager.create_user(
            'tokenloginviewtest-existinguser')

    def test_redirects_to_home(self):
        """The view should eventually redirect to the homepage.

        """
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('home'))

    def test_valid_token(self):
        """A valid token can be used to log in.

        """
        token = self.generator.make_token(self.existing_user.get_username())
        self.client.get(self.url, data={'token': token})
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_invalid_token(self):
        """An invalid token cannot be used to log in.

        """
        self.client.get(self.url, data={'token': 'invalid_token'})
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_new_user_can_login(self):
        """A visitor without a user object can login with valid token.

        """
        # pylint: disable=protected-access
        with self.assertRaises(USER.DoesNotExist):
            USER._default_manager.get_by_natural_key(self.new_username)

        token = self.generator.make_token(self.new_username)
        self.client.get(self.url, data={'token': token})
        self.assertTrue(get_user(self.client).is_authenticated)
        USER._default_manager.get_by_natural_key(self.new_username)


class SendTokenViewTest(TestCase):
    """Tests for the view which sends the login email.

    """
    def setUp(self):
        self.url = reverse('send_token')
        self.test_email = 'sendtokenviewtest-newvisitor@example.com'

    def test_invalid_input_show_error(self):
        """If a non email is posted redirect with error.

        """
        response = self.client.post(self.url, data={'email': 'invalidinput'},
                                    follow=True)
        self.assertContains(response, 'Enter a valid email address.')

    def test_redirects_send_token_done(self):
        """The send_login_email url redirects to success page.

        """
        response = self.client.post(self.url, data={'email': self.test_email},
                                    follow=True)
        self.assertContains(response, 'Check your email')

    def test_view_sends_token_email(self):
        """The view should send an email to the email address from post.

        """
        self.client.post(self.url, data={'email': self.test_email})
        self.assertEqual(mail.outbox[0].to, [self.test_email])
