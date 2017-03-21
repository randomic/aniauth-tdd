"""accounts app unittests for tokens

"""
import base64
from time import sleep

from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.tokens import LoginTokenGenerator


USER = get_user_model()


class TokenGeneratorTest(TestCase):
    """Tests for login token model.

    """
    def setUp(self):
        self.test_email = 'newvisitor@example.com'
        self.generator = LoginTokenGenerator()

    def test_unique_tokens_generated(self):
        """Tokens generated one second apart should differ.

        """
        token1 = self.generator.make_token(self.test_email)
        sleep(1)
        token2 = self.generator.make_token(self.test_email)
        self.assertNotEqual(token1, token2)

    def test_email_recovered_from_token(self):
        """A consumed token should yield the original user.

        """
        token = self.generator.make_token(self.test_email)
        email = self.generator.consume_token(token)
        self.assertEqual(email, self.test_email)

    def test_modified_token_fails(self):
        """A modified token returns None instead of a user.

        """
        token = self.generator.make_token(self.test_email)

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
        """A token which has expired returns None instead of a user.

        """
        token = self.generator.make_token(self.test_email)
        sleep(1)  # Ensure the token is more than 0 seconds old.
        email = self.generator.consume_token(token, 0)
        self.assertIsNone(email)

    def test_random_string_fails(self):
        """A random non-token string returns None instead of a user.

        """
        token = USER.objects.make_random_password()
        email = self.generator.consume_token(token)
        self.assertIsNone(email)

    def test_tokenlike_string_fails(self):
        """A random token-like string returns None instead of a user.

        """
        token = base64.urlsafe_b64encode(
            USER.objects.make_random_password().encode()
        ).decode()
        email = self.generator.consume_token(token)
        self.assertIsNone(email)
