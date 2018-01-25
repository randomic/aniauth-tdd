"""Backend for logintokens authentication.

"""
from django.contrib.auth import get_user_model

from logintokens.tokens import default_token_generator


USER = get_user_model()


class EmailOnlyAuthenticationBackend:
    """Authenticates by consuming a provided login token.

    """
    token_generator = default_token_generator

    def authenticate(self, unused_request, token=None, max_age=600):
        """Login/create the user from the provided login token.

        """
        # pylint: disable=protected-access
        result = self.token_generator.consume_token(token, max_age)
        if result:
            username, login_timestamp = result.split(self.token_generator.sep)
            try:
                user = USER._default_manager.get_by_natural_key(
                    username)
                _login_timestamp = ('' if user.last_login is None
                                    else str(int(user.last_login.timestamp())))
                if login_timestamp == _login_timestamp:
                    return user
            except USER.DoesNotExist:
                user = USER._default_manager.create_user(
                    username, username)
                return user

    @staticmethod
    def get_user(user_id):
        """Return user object from primary key id.

        """
        # pylint: disable=protected-access
        try:
            return USER._default_manager.get(pk=user_id)
        except USER.DoesNotExist:
            return None
