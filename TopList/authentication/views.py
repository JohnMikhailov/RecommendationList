import jwt

from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from TopList import settings
from authentication.utils import create_token
from user.serializers import CustomUserSerializer
from user.models import CustomUser
from authentication.serializers import AuthorizationSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    user_serializer = CustomUserSerializer(data=request.data)
    user_serializer.is_valid(raise_exception=True)
    user_serializer.save()
    return Response(user_serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):

    credentials = request.data
    authorization_serializer = AuthorizationSerializer(data=credentials)
    authorization_serializer.is_valid(raise_exception=True)
    username = credentials['username']
    password = credentials['password']

    user = CustomUser.objects.filter(username=username).first()
    if not user:
        raise AuthenticationFailed()

    if not check_password(password, user.password):
        raise AuthenticationFailed()

    payload = {'id': user.id, 'email': user.email}
    access_token = create_token(payload, token_type='access')
    refresh_token = create_token(payload, token_type='refresh')

    user.refresh_token = refresh_token
    user.save()
    return Response(data={'access': access_token, 'refresh': refresh_token})


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh(request):
    credentials = request.data
    refresh_token_credentials = credentials.get('refresh_token', None)
    if not refresh_token_credentials:
        raise AuthenticationFailed("Invalid token name. 'refresh_token' - required")
    try:
        payload = jwt.decode(refresh_token_credentials, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token header')

    id_ = payload.get('id', None)

    user = CustomUser.objects.get(pk=id_)
    if not user:
        raise AuthenticationFailed('User not found')

    refresh_token = user.refresh_token
    if refresh_token != refresh_token_credentials:
        raise AuthenticationFailed('Token not match')

    payload = {'id': user.id, 'email': user.email}
    access_token = create_token(payload, token_type='access')
    refresh_token = create_token(payload, token_type='refresh')

    user.refresh_token = refresh_token
    user.save()
    return Response(data={'access': access_token, 'refresh': refresh_token})
