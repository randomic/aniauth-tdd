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

    def make_token(self, email):
        """Return a login token for the provided email.

        """
        return base64.urlsafe_b64encode(
            self.signer.sign(email).encode()
        ).decode()

    def consume_token(self, token, max_age=600):
        """Extract the user provided the token isn't older than max_age.

        """
        try:
            return self.signer.unsign(
                base64.urlsafe_b64decode(token.encode()), max_age
            )
        except (BadSignature, base64.binascii.Error):
            return None
