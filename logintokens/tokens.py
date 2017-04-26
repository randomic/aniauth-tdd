"""module containing generator for login tokens

"""
import base64

from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner, BadSignature


USER = get_user_model()


class LoginTokenGenerator:
    """Generator for the timestamp signed tokens used for logging in.

    """
    def __init__(self):
        self.signer = TimestampSigner(
            salt='aniauth-tdd.accounts.token.LoginTokenGenerator')

    def make_token(self, username):
        """Return a login token for the provided email.

        """
        try:
            user = USER.objects.get(username=username)
            login_timestamp = ('' if user.last_login is None
                               else int(user.last_login.timestamp()))
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
            result = self.signer.unsign(
                base64.urlsafe_b64decode(token.encode()), max_age
            )
        except (BadSignature, base64.binascii.Error):
            return None

        username, login_timestamp = result.split(self.signer.sep)
        try:
            user = USER.objects.get(username=username)
            user_login_timestamp = ('' if user.last_login is None
                                    else int(user.last_login.timestamp()))
            if user_login_timestamp == login_timestamp:
                return username
            else:
                return None  # The user has logged in since this token was made
        except USER.DoesNotExist:
            return username
