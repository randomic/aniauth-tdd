"""module containing generator for login tokens

"""
import base64

from django.core.signing import TimestampSigner, BadSignature
from django.contrib.auth import get_user_model


class LoginTokenGenerator:
    """Generator for the timestamp signed tokens used for logging in.

    """
    def __init__(self):
        self.signer = TimestampSigner(
            salt='aniauth-tdd.accounts.token.LoginTokenGenerator')

    def create_token(self, user):
        """Return a login token for the provided user.

        """
        return base64.urlsafe_b64encode(
            self.signer.sign(user.email).encode()
        ).decode()

    def consume_token(self, token, max_age=600):
        """Extract the user provided the token isn't older than max_age.

        """
        try:
            email = self.signer.unsign(
                base64.urlsafe_b64decode(token.encode()), max_age
            )
            return get_user_model().objects.get(email=email)
        except (BadSignature,
                base64.binascii.Error,
                get_user_model().DoesNotExist):
            return None
