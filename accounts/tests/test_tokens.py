"""accounts app unittests for tokens

"""
import base64
from time import sleep

from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.tokens import LoginTokenGenerator


USER = get_user_model()
TEST_EMAIL = 'newvisitor@example.com'


class TokenGeneratorTest(TestCase):
    """Tests for login token model.

    """
    def setUp(self):
        self.user = USER.objects.create_user(TEST_EMAIL)
        self.generator = LoginTokenGenerator()

    def test_unique_tokens_generated(self):
        """Tokens generated one second apart should differ.

        """
        token1 = self.generator.create_token(self.user)
        sleep(1)
        token2 = self.generator.create_token(self.user)
        self.assertNotEqual(token1, token2)

    def test_email_recovered_from_token(self):
        """A consumed token should yield the original user.

        """
        token = self.generator.create_token(self.user)
        user = self.generator.consume_token(token)
        self.assertEqual(user, self.user)

    def test_modified_token_fails(self):
        """A modified token returns None instead of a user.

        """
        token = self.generator.create_token(self.user)

        # Modify the email address which is 'signed'.
        split_token = base64.urlsafe_b64decode(
            token.encode()
        ).decode().split('@')

        split_token[0] = 'maliciousvisitor'
        malicious_token = base64.urlsafe_b64encode(
            '@'.join(split_token).encode()
        ).decode()

        self.assertIsNone(self.generator.consume_token(malicious_token))

    def test_deleted_token_fails(self):
        """A token yielding an email belonging to deleted user returns none.

        """
        token = self.generator.create_token(self.user)
        self.user.delete()
        self.assertIsNone(self.generator.consume_token(token))

    def test_expired_token_fails(self):
        """A token which has expired returns None instead of a user.

        """
        token = self.generator.create_token(self.user)
        sleep(1)  # Ensure the token is more than 0 seconds old.
        user = self.generator.consume_token(token, 0)
        self.assertIsNone(user)

    def test_random_string_fails(self):
        """A random non-token string returns None instead of a user.

        """
        token = USER.objects.make_random_password()
        user = self.generator.consume_token(token)
        self.assertIsNone(user)

    def test_tokenlike_string_fails(self):
        """A random token-like string returns None instead of a user.

        """
        token = base64.urlsafe_b64encode(
            USER.objects.make_random_password().encode()
        ).decode()
        user = self.generator.consume_token(token)
        self.assertIsNone(user)
