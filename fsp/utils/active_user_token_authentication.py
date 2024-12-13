from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class ActiveUserTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        if not user.is_active:
            raise AuthenticationFailed('Ваш аккаунт не активирован. Пожалуйста, активируйте его.')
        return user, token