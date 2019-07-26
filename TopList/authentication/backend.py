import jwt
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from TopList import settings
from user.models import CustomUser


class JWTAuth(object):

    def authenticate(self, request):
        auth = get_authorization_header(request).decode('utf-8').split()

        if not auth or auth[0].lower() != 'jwt':
            raise AuthenticationFailed()

        try:
            payload = jwt.decode(auth[1], settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            msg = 'Invalid token'
            raise AuthenticationFailed(msg)

        return self.authenticate_credentials(payload)

    def authenticate_credentials(self, payload):
        username = payload.get('username', None)
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist as exc:
            raise AuthenticationFailed(str(exc))

        if not user.is_active:
            raise AuthenticationFailed('User is inactive or deleted')

        return user, payload
