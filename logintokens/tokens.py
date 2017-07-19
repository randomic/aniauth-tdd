"""module containing generator for login tokens

"""
import base64

from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner, BadSignature


USER = get_user_model()


class LoginTokenGenerator:
    """Generator for the timestamp signed tokens used for logging in.

    """
    signer = TimestampSigner(
        salt='aniauth-tdd.accounts.token.LoginTokenGenerator')
    sep = signer.sep

    def make_token(self, username):
        """Return a login token for the provided email.

        """
        try:
            # pylint: disable=protected-access
            user = USER._default_manager.get_by_natural_key(username)
            login_timestamp = ('' if user.last_login is None
                               else str(int(user.last_login.timestamp())))
        except USER.DoesNotExist:
            login_timestamp = ''

        value = str('%s%s%s') % (username, self.signer.sep, login_timestamp)
        return base64.urlsafe_b64encode(
            self.signer.sign(value).encode()
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


default_token_generator = LoginTokenGenerator()
