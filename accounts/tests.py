"""accounts app unittests

"""
from time import sleep

from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.token import LoginTokenGenerator

TEST_EMAIL = 'newvisitor@example.com'


class WelcomePageTest(TestCase):
    """Tests relating to the welcome_page view.

    """
    def test_uses_welcome_template(self):
        """The root url should response with the welcome page template.

        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'accounts/welcome.html')


class UserModelTest(TestCase):
    """Tests for passwordless user model.

    """
    def test_user_valid_with_only_email(self):
        """Should not raise if the user model is happy with email only.

        """
        user = get_user_model()(email=TEST_EMAIL)
        user.full_clean()

    def test_users_are_authenticated(self):
        """User objects should be authenticated for views/templates.

        """
        user = get_user_model()()
        self.assertTrue(user.is_authenticated())


class TokenGeneratorTest(TestCase):
    """Tests for login token model.

    """
    def setUp(self):
        self.signer = LoginTokenGenerator()

    def test_unique_tokens_generated(self):
        """Tokens generated one second apart should differ.

        """
        token1 = self.signer.create_token(TEST_EMAIL)
        sleep(1)
        token2 = self.signer.create_token(TEST_EMAIL)
        self.assertNotEqual(token1, token2)

    def test_email_recovered_from_token(self):
        """A consumed token should yield the original email address.

        """
        token = self.signer.create_token(TEST_EMAIL)
        email = self.signer.consume_token(token)
        self.assertEqual(email, TEST_EMAIL)
