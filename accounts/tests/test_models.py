"""accounts app unittests for models

"""
from django.test import TestCase
from django.contrib.auth import get_user_model


USER = get_user_model()
TEST_EMAIL = 'newvisitor@example.com'


class UserModelTest(TestCase):
    """Tests for passwordless user model.

    """
    def test_user_valid_with_only_email(self):
        """Should not raise if the user model is happy with email only.

        """
        user = USER(email=TEST_EMAIL)
        user.full_clean()

    def test_users_are_authenticated(self):
        """User objects should be authenticated for views/templates.

        """
        user = USER()
        self.assertTrue(user.is_authenticated())
