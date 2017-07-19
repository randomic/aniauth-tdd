"""logintokens app unittests for backends

"""
from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate

from logintokens.tokens import default_token_generator
from logintokens.tests.util import MOCK_TIME as mock_time


USER = get_user_model()


@patch('time.time', mock_time.time)
class EmailOnlyAuthenticationBackendTest(TestCase):
    """Tests for email only authentication backend

    """
    def setUp(self):
        # pylint: disable=protected-access
        self.generator = default_token_generator
        self.new_username = 'emailonlyauthenticationbackendtest-newvisitor'
        self.existing_user = USER.objects.create_user(
            'emailonlyauthenticationbackendtest-existinguser')

    def test_different_tokens_usable(self):
        """Two differing tokens should both be valid to authenticate.

        """
        username = self.existing_user.get_username()
        token1 = self.generator.make_token(username)
        mock_time.sleep(60)
        token2 = self.generator.make_token(username)

        self.assertNotEqual(token1, token2)
        self.assertEqual(authenticate(token=token1), self.existing_user)
        self.assertEqual(authenticate(token=token2), self.existing_user)

    def test_login_invalidates_tokens(self):
        """Tokens generated before a successful login should become invalid.

        """
        username = self.existing_user.get_username()
        token1 = self.generator.make_token(username)
        mock_time.sleep(60)
        token2 = self.generator.make_token(username)

        self.assertNotEqual(token1, token2)

        self.client.force_login(self.existing_user)

        self.assertIsNone(authenticate(token=token1))
        self.assertIsNone(authenticate(token=token2))

    def test_new_visitor_creates_user(self):
        """Using a token from a new visitor should create their user object.

        """
        token = self.generator.make_token(self.new_username)
        user = authenticate(token=token)
        self.assertIsInstance(user, USER)
