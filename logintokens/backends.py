from django.contrib.auth import get_user_model

from logintokens.tokens import default_token_generator


USER = get_user_model()



class EmailOnlyAuthenticationBackend:
    token_generator = default_token_generator

    def authenticate(self, request, token=None, max_age=600):
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

    def get_user(self, user_id):
        try:
            return USER._default_manager.get(pk=user_id)
        except USER.DoesNotExist:
            return None
