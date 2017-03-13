"""accounts app unittests

"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import LoginToken


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


class TokenModelTest(TestCase):
    """Tests for login token model.

    """
    def test_unique_tokens_generated(self):
        """Two tokens generated should be unique.

        """
        token1 = LoginToken(TEST_EMAIL)
        token2 = LoginToken(TEST_EMAIL)
        self.assertNotEqual(token1, token2)
