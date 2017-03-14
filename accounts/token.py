"""module containing generator for login tokens

"""
import base64

from django.core.signing import TimestampSigner, BadSignature


class LoginTokenGenerator(object):
    """Generator for the timestamp signed tokens used for logging in.

    """
    def __init__(self):
        self.signer = TimestampSigner(
            salt='aniauth-tdd.accounts.token.LoginTokenGenerator')

    def create_token(self, email):
        """Return a login token for the provided email address.

        """
        return base64.urlsafe_b64encode(
            self.signer.sign(email).encode()
        ).decode()

    def consume_token(self, token, max_age=600):
        """Extract the email provided the token isn't older than max_age.

        """
        try:
            return self.signer.unsign(
                base64.urlsafe_b64decode(token.encode()), max_age
            )
        except BadSignature:
            return None
