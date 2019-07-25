import jwt
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from user.models import CustomUser


class JWTAuth(object):

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != 'jwt':
            return None

        try:
            payload = jwt.decode(auth[1], 'secretKey', algorithms=['HS256'])
        except jwt.InvalidTokenError:
            msg = 'Invalid token header'
            raise AuthenticationFailed(msg)

        return self.authenticate_credentials(payload)

    def authenticate_credentials(self, payload):
        username = payload.get('username', None)

        try:
            user = CustomUser.objects.get(username=username)
        except ModuleNotFoundError:
            raise AuthenticationFailed('Token is invalid')

        if not user.is_active:
            raise AuthenticationFailed('User is inactive or deleted')

        return user, payload
