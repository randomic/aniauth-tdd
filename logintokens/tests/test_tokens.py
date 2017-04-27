"""logintokens app unittests for tokens

"""
import base64
from time import sleep

from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from logintokens.tokens import default_token_generator


USER = get_user_model()


class TokenGeneratorTest(TestCase):
    """Tests for login token generator.

    """
    def setUp(self):
        self.client = Client()
        self.new_username = 'newvisitor'
        self.existing_user = USER.objects.create_user('existinguser')
        self.generator = default_token_generator

    def test_unique_tokens_generated(self):
        """Tokens generated one second apart should differ.

        """
        token1 = self.generator.make_token(self.new_username)
        sleep(1)
        token2 = self.generator.make_token(self.new_username)
        self.assertNotEqual(token1, token2)

    def test_existing_user_token(self):
        """A consumed token should yield the original username.

        """
        token = self.generator.make_token(self.existing_user.get_username())
        result = self.generator.consume_token(token)
        expected_result = '{}{}'.format(
            self.existing_user.get_username(),
            self.generator.sep)
        self.assertEqual(result, expected_result)

    def test_new_user_token(self):
        """A token which doesn't yet have a user should yield the username.

        """
        token = self.generator.make_token(self.new_username)
        result = self.generator.consume_token(token)
        expected_result = '{}{}'.format(
            self.new_username,
            self.generator.sep)
        self.assertEqual(result, expected_result)

    def test_token_reuse(self):
        """A token must be made invalid as soon as a user logs in.

        """
        token1 = self.generator.make_token(self.existing_user.get_username())
        self.client.force_login(self.existing_user)
        token2 = self.generator.make_token(self.existing_user.get_username())
        self.assertNotEqual(token1, token2)

    def test_modified_token_fails(self):
        """A modified token returns None instead of a username.

        """
        token = self.generator.make_token(self.new_username)

        # Modify the email address which is 'signed'.
        split_token = base64.urlsafe_b64decode(
            token.encode()
        ).decode().split('@')

        split_token[0] = 'maliciousvisitor'
        malicious_token = base64.urlsafe_b64encode(
            '@'.join(split_token).encode()
        ).decode()

        self.assertIsNone(self.generator.consume_token(malicious_token))

    def test_expired_token_fails(self):
        """A token which has expired returns None instead of a username.

        """
        token = self.generator.make_token(self.new_username)
        sleep(1)  # Ensure the token is more than 0 seconds old.
        username = self.generator.consume_token(token, 0)
        self.assertIsNone(username)

    def test_random_string_fails(self):
        """A random non-token string returns None instead of a username.

        """
        token = USER.objects.make_random_password()
        username = self.generator.consume_token(token)
        self.assertIsNone(username)

    def test_tokenlike_string_fails(self):
        """A random token-like string returns None instead of a username.

        """
        token = base64.urlsafe_b64encode(
            USER.objects.make_random_password().encode()
        ).decode()
        username = self.generator.consume_token(token)
        self.assertIsNone(username)
