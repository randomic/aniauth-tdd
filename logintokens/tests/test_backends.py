"""logintokens app unittests for backends

"""
from time import sleep

from django.test import TestCase, Client
from django.contrib.auth import get_user_model, authenticate

from logintokens.tokens import default_token_generator


USER = get_user_model()


class EmailOnlyAuthenticationBackendTest(TestCase):
    """Tests for email only authentication backend

    """
    def setUp(self):
        self.client = Client()
        self.generator = default_token_generator
        self.new_username = 'newvisitor'
        self.existing_user = USER._default_manager.create_user('existinguser')

    def test_different_tokens_usable(self):
        """Two differing tokens should both be usabe to authenticate.

        """
        username = self.existing_user.get_username()
        token1 = self.generator.make_token(username)
        sleep(1)
        token2 = self.generator.make_token(username)

        self.assertNotEqual(token1, token2)
        self.assertEqual(authenticate(token=token1), self.existing_user)
        self.assertEqual(authenticate(token=token2), self.existing_user)

    def test_login_invalidates_tokens(self):
        """Tokens generated before a successful login should become invalid.

        """
        username = self.existing_user.get_username()
        token1 = self.generator.make_token(username)
        sleep(1)
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
