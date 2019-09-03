import jwt
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from TopList import settings
from user.models import CustomUser


class JWTAuth(BaseAuthentication):

    def authenticate(self, request):
        header = get_authorization_header(request)
        if not header:
            return None

        auth = header.decode('utf-8').split()

        if auth[0].lower() != 'jwt':
            raise AuthenticationFailed()

        try:
            payload = jwt.decode(auth[1], settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            msg = 'Invalid token'
            raise AuthenticationFailed(msg)

        return self.authenticate_credentials(payload)

    def authenticate_credentials(self, payload):
        id_ = payload.get('id', None)
        try:
            user = CustomUser.objects.get(pk=id_)
        except CustomUser.DoesNotExist as exc:
            raise AuthenticationFailed(str(exc))

        if not user.is_active:
            raise AuthenticationFailed('User is inactive or deleted')

        return user, payload

    def authenticate_header(self, request):
        return 'jwt'
